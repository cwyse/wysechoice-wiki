---
title: Backup and Restore
description: 
published: true
date: 2020-12-21T02:06:27.335Z
tags: 
editor: markdown
dateCreated: 2020-12-18T03:10:24.783Z
---


# User Data Backups

User backups are handled in three separate ways.
1. Frequent backups to the QNAP NAS server
2. Long term backups to Google Drive
3. Long term backups to Amazon Glacier

## QNAP NAS Backups

TBD

# Google Drive Backups
These backups are intended to be for relatively long term storage.  It's meant to be used if the NAS backup fails.  The backup is initiated from the QNAP NAS.  It runs a scheduled backup to Google Drive once per week.  Backups are stored in a subdirectory of "My Drive/QNAP_Backup".  The backups use the chris.wyse.1965@gmail.com Google account.

Backup Host: qnap.wysechoice.net
Backup Server: drive.google.com
Backup Server Account: chris.wyse.1965@gmail.com
Backup Utility (on host): HBS 3 Hybrid Backup Sync
Data Compression: None
Client Side Encryption Cipher: aes-256-cbc
Message digest: md5
Encryption Password: <store securely outside the repository>

The files are sent to Google Drive after encryption.  The directory structure is maintained, but the specific files will not be available until they are decrypted.  The command to decrypt is:
```
openssl enc -md md5 -aes-256-cbc -d -in <encrypted file> -out <decrypted file>
```
# Amazon Glacier Backup

These backups are intended for very long term storage.  Retrieval is extremely slow (although storage is very cheap).  This is a last resort to recover data.

Like the Google Drive backup, it is initiated from the QNAP NAS.  It runs a scheduled backup to Amazon Glacier once per month.  Backups are stored in a an Amazon vault, 'QNAP_Vault'.  The backups use the chris.wyse@wysechoice.net Amazon account.

Backup Host: qnap.wysechoice.net
Backup Server: aws.amazon.com
Backup Server Account: chris.wyse@wysechoice.net
AWS Access Key ID: <store securely outside the repository>
AWS Secret Access Key: <store securely outside the repository>
AWS Region: us-east-1
Backup Utility (on host): HBS 3 Hybrid Backup Sync
Data Compression: None
Client Side Encryption Cipher: aes-256-cbc
Message digest: md5
Encryption Password: <store securely outside the repository>

Retrieval and deletion requires scripting.  The AWS CLI must be installed, and credentials stored in ~/.aws/credentials, with the config file in ~/.aws/config.

## Retrieval

The files are retrieved via the Amazon CLI using *aws glacier* commands.  The retrieval process is still TBD.

The files are sent to Amazon after encryption.  The directory structure is maintained, but the specific files will not be available until they are decrypted.  The command to decrypt is:
```
openssl enc -md md5 -aes-256-cbc -d -in <encrypted file> -out <decrypted file>
```

## Deletion

Deletion of all archives in the vault may take hours or days.  The easiest was to accomplish the is to run a the script below.  The script requests a list of archives to delete.  It polls for the list every 10 minutes until it is received.  Once received, it issues a delete command for each of the archives found, then deletes the vault.

```
#!/bin/bash

aws_account_id=741335856197
aws_region=us-east-1
aws_vault_name=QNAP_Vault
cron_interval=10

script_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"

declare -A print_levels=([TRACE]=0 [DEBUG]=1 [INFO]=2 [WARN]=3 [ERROR]=4)
print_level="TRACE"
aws_echo=0  

printLevel() {
    local _log_priority=$1
    local _log_format="${@:2:1}"
    local _log_message="${*:3}"

    #check if level exists
    [[ ${print_levels[${_log_priority}]} ]] || return 1

    #check if level is enough
    (( ${print_levels[${_log_priority}]} < ${print_levels[${print_level}]} )) && return 2
 
    case ${_log_priority} in
    	TRACE|DEBUG|ERROR)
    		printf "%s (%s:%d): " "${_log_priority}" "${FUNCNAME[1]}" ${BASH_LINENO[0]}  >/dev/stderr
    		;;
    	INFO|WARN)
    		printf "%s: " "${_log_priority}" >/dev/stderr
    		;;
    esac

    printf "${_log_format}" ${_log_message} >/dev/stderr

}

awsCmd() {
	printLevel "TRACE" "aws ${*}\n"
	if [ -n "${aws_echo}" -a ${aws_echo} -ne 0 ]; then
		local _aws_out=$(mktemp)
		aws "$@" >${_aws_out}
		cat ${_aws_out} >/dev/stderr
		cat ${_aws_out}
		rm ${_aws_out}
	else
		aws "$@" 
	fi
}

isJobComplete() {
	printLevel "TRACE" "%s\n" "$@"
    local _jobs_file=$(mktemp)
	awsCmd glacier describe-job --vault-name ${aws_vault_name} --account-id ${aws_account_id} --job-id ${job_id} >${_jobs_file}
	local _completed=$(cat ${_jobs_file} | jq '.Completed')
	if [[ "${_completed}" == "true" ]]; then
		completion_date=$(cat ${_jobs_file} | jq '.CompletionDate' )
		printLevel "INFO" "isJobComplete: completion_date = %s\n" ${completion_date}
		rm ${_jobs_file}
		return 0
	else
		rm ${_jobs_file}
		return 1
	fi
}

getInventoryJobId() {
	printLevel "TRACE" "%s\n" "$@"
    _jobs_file=$(mktemp)
    awsCmd glacier list-jobs --vault-name ${aws_vault_name} --account-id ${aws_account_id} >${_jobs_file}
	job_id=$(cat ${_jobs_file} | jq ".JobList[0] | select(.StatusCode == \"InProgress\") | select(.Action == \"InventoryRetrieval\") | select(.VaultARN | contains(\"${aws_vault_name}\")) .JobId")
	creation_date=$(cat ${_jobs_file} | jq ".JobList[0] | select(.StatusCode == \"InProgress\") | select(.Action == \"InventoryRetrieval\") | select(.VaultARN | contains(\"${aws_vault_name}\")) .CreationDate")
	rm ${_jobs_file}
	if [ -n "${job_id}" ]; then
		printLevel "INFO" "Inventory JobId = %s\n" ${job_id}
		printLevel "INFO" "CreationDate    = %s\n" ${creation_date}
	else
		printLevel "INFO" "getInventoryJobId: job_id = <Not Found>\n" 
	fi
}

startInventory() {
	printLevel "TRACE" "%s\n" "$@"
	job_id=$(awsCmd glacier initiate-job --job-parameters '{"Type": "inventory-retrieval"}' --vault-name ${aws_vault_name} --account-id ${aws_account_id} --region ${aws_region} | jq '.jobId')
	printLevel "INFO" "job_id = %s\n" ${job_id}
}

setNextState() {
	printLevel "TRACE" "%s\n" "$@"
    # State is always the first parameter passed
    if [ -n "$1" ]; then  	
  		next_state=$1
  	else
    	getInventoryJobId
    	if [ -n "${job_id}" ]; then
      		# Job is in progress
      		next_state="STATUS"
    	else
      		# Inventory isn't running, so check to see if we were waiting for it to complete
      		cron_finish=$(cronSearch "0 0 1 1")
      		if [ -n "${_cron_finish}" ]; then
      			next_state="FINISH"
      		else
        		next_state="START"
      		fi
    	fi
  	fi
	printLevel "TRACE" "Next State = ${next_state}\n"
}

advanceState() {
	printLevel "TRACE" "%s\n" "$@"
	state=${next_state}
}

cronAdd() {
	printLevel "TRACE" "%s\n" "$@"
	# Schedule cronjob
	local _cron_file=$(mktemp)
	crontab -l >${_cron_file}
	printf "${1}\n" >> ${_cron_file}
	crontab ${_cron_file}
	cat ${_cron_file}
	rm ${_cron_file}
}

cronDel() {
	printLevel "TRACE" "%s\n" "$@"
	# Remove cronjob
	local _cron_file=$(mktemp)
	crontab -l | grep -v "${1}" >${_cron_file}
	crontab ${_cron_file}
	cat ${_cron_file}
	rm ${_cron_file}
}

cronSearch() {
	printLevel "TRACE" "%s\n" "$@"
	# Search cron table
    crontab -l | grep "${1}"
}

getJobOutput() {
	printLevel "TRACE" "%s\n" "$@"
	local _job_output=$(mktemp)
	awsCmd glacier get-job-output --vault-name ${aws_vault_name} --account-id ${aws_account_id} --region ${aws_region} --job-id ${job_id} ${_job_output}
	printf "%s" ${_job_output} 
	rm ${_job_output}
}

deleteArchives() {
	printLevel "TRACE" "%s\n" "$@"
    local _job_output="$(getJobOutput)"
	local _archive_ids=$(jq .ArchiveList[].ArchiveId < ${_job_output})
	archive_count=$(echo ${_archive_ids} | wc -w)
	local _loop_cnt=0
	for _archive_id in ${_archive_ids}; do
		_loop_cnt=$(( ${_loop_cnt} + 1 ))
	    awsCmd glacier delete-archive --archive-id=${archive_id} --vault-name ${aws_vault_name} --account-id ${aws_account_id} --region ${aws_region}
	done
}

printCompletionStats() {
	printLevel "TRACE" "%s\n" "$@"
    printLevel "INFO" "Job id %s started at %s, deleted %d archives from %s, and completed at %s\n" ${job_id} ${creation_date} ${archive_count} ${aws_vault_name} ${completion_date}
}

processState() {
	printLevel "TRACE" "%s\n" "$@"
	case ${state} in
		START)
    		# Initiate inventory and move to WAIT state
    		printf "Request Inventory?"
    		read
    		startInventory
    		# Delete any existing cronjobs
    		cronDel "${script_path}"
    		setNextState "WAIT"
    		# Schedule this to run again in ${cron_interval} minutes
    		cronAdd "*/${cron_interval} * * * * ${script_path} WAIT ${job_id} ${creation_date} ${archive_count} ${completion_date}"
    		exit
    		;;
  		STATUS)
    		# Display how long we've been waiting
            printLevel "INFO" "Inventory started at %s, job id %s.\n" "${creation_date} ${job_id}"
            printLevel "INFO" "Testing every %d minutes.\n" ${cron_interval}
            exit
    		;;
  		WAIT)
    		# If job_id is complete, advance to COMPLETE state
    		if isJobComplete; then
    			setNextState "COMPLETE"
    			local _cron_rule=$(cronSearch "${cron_task}")
    			cronDel "${_cron_rule}"
    		else
    			exit
    		fi
    		;;
  		COMPLETE)
    		# Delete archives, advance to FINISH state
    		deleteArchives
    		# Schedule cronjob to display output on 1/1 (it will be deleted if the user checks the status)
    		cronAdd "0 0 1 1 * ${script_path} FINISH ${job_id} ${creation_date} ${archive_count} ${completion_date}"
    		exit
    		;;
  		FINISH)
			if [ -z "${1}" ]; then
				local _last_args=$(printf "%s" "$(printf "%s" "${cron_finish}" | cut -f 6- -d ' ')")
				${script_path} ${_last_args}
			fi
			cronDel "0 0 1 1"
			;;
	esac
}

getArgs() {
	printLevel "TRACE" "%s\n" "$@"
    setNextState ${1}
    job_id=${job_id:-${2}}
    creation_date=${creation_date:-${3}}
    archive_count=${archive_count:-${4}}
    completion_date=${completion_date:-${5}}
}

main() {
    printLevel "INFO" "Started ${script_path} $@\n\n"
	printLevel "TRACE" "%s\n" "$@"

	# Global variables
	declare -g job_id
	declare -g creation_date
	declare -g archive_count
	declare -g completion_date
	declare -g cron_finish

    getArgs $@
    cron_task="${script_path} $@"

    while : ; do
	    advanceState
	    processState
        [[ "${state}" != "FINISH" ]] || break
    done
    printLevel "INFO" "Finished ${script_path} $@\n\n"
}

main $@

exit
```

> The docker image information in yellow below did not complete successfully.  The shell script above was created to address the problem.  The content below is left as a reference only.
{.is-danger}


> Deletion of all archives in the vault may take hours or days.  The easiest was to accomplish the is to run a docker image.  The image requests a list of archives to delete.  It polls for the list every 10 minutes until it is received.  Once received, it issues a delete command for each of the archives found, then deletes the vault.
> 
> ```
> #!/bin/bash
> 
> AWS_ACCOUNT_ID=741335856197
> AWS_REGION=us-east-1
> AWS_VAULT_NAME=QNAP_Vault
> AWS_OUTPUT='./output.json'
> 
> AWS_CREDENTIALS_JSON='/home/chris/.aws/credentials.json'
> 
> # https://github.com/leeroybrun/glacier-vault-remove
> #docker run -v ${AWS_CREDENTIALS_JSON}:/app/credentials.json -d leeroyb/glacier-vault-remove ${AWS_REGION} [${AWS_VAULT_NAME}|LIST] [DEBUG] [NUM_PROCESSES] [<job_id>|LIST|NEW|LATEST]
> docker run -v ${AWS_CREDENTIALS_JSON}:/app/credentials.json -d leeroyb/glacier-vault-remove ${AWS_REGION} ${AWS_VAULT_NAME} DEBUG 10
> ```
> 
> The credentials for the deletion script should be in JSON format:
> ```
> {
> 	"AWSAccessKeyId": "<store securely outside the repository>",
> 	"AWSSecretKey":   "<store securely outside the repository>"
> }
> ```
> The credentials for the CLI:
{.is-warning}

```
[default]
aws_access_key_id=<store securely outside the repository>
aws_secret_access_key=<store securely outside the repository>
```
The config for the CLI:
```
[default]
region=us-east-1
output=json
```

# Network Configuration Backup

Network configuration backup is handled separately from user data backup.  The LibreNMS application is used to consolidate various configurations.  

LibreNMS will probably back up to GitLab.  It will run as a stack of docker containers, which will be used for additional network support, like reverse proxy, syslog server, and other network tools.


# General Backup
**Current backup location**: chris-Precision-7740:/home/chris/personal/backups

# Postgres Backup
**Current backup location**: <postgres_host>:~/docker_vols/postgres

### Complete Database Backup / Restore
The `<postgres-username>` should be the owner of the postgres database.  Usually *postgres* is the owner of the postgres database.
  
```
$ # Dump database to <backup-clean-file>
$ pg_dumpall --verbose --clean --host=<postgres-server> --port 5432 --username=<postgres-username> --file=<backup-clean-file>
$
$ # Restore database from <backup-clean-file>, dropping existing tables
$ psql --host=<postgres-server> --port 5432 --file=<backup-clean-file> --dbname=postgres --echo-all --log-file=<backup-clean-log-file> --output=<backup-clean-output-file> --username=<postgres-username>
$
$ # Dump database to <backup-file>
$ pg_dumpall --verbose --host=<postgres-server> --port 5432 --username=<postgres-username> --file=<backup-file>
$
$ # Restore all databases from <backup-file>
$ psql --host=<postgres-server> --port 5432 --file=<backup-file> --dbname=postgres --echo-all --log-file=<backup-log-file> --output=<backup-output-file> --username=<postgres-username>
```
Example backup:

- postgres-server:  192.168.40.30
- postgres-username: postgres
- backup-clean-file: backup.clean.file
- ~/.pgpass:
    - 192.168.40.30:5432:*:wikijs:wikijsrocks
    
```
$ pg_dumpall --verbose --clean --host 192.168.40.30 --port 5432 --username postgres --file backup.clean.file
```
Example restore:

- postgres-server:  192.168.40.30
- postgres-username: xwiki
- backup-clean-file: backup.clean.file
- ~/.pgpass:
    - 192.168.40.30:5432:*:wikijs:wikijsrocks

```
$ psql --host=192.168.40.30 --port 5432 --file=backup.clean.file --dbname=postgres --echo-all --log-file=backup.clean.file.log --output=backup.clean.file.out -U xwiki
```
You need to restart the postgres server to update the ownership of the databases.