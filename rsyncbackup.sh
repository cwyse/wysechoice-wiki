#!/bin/bash
#set -x
set -e
# Configuration variables (change as you wish)
remote="${1:-ssh_remote}"                                         # Remote IP address of source
srcmodel="/${2:-chris}"
srcpath="/${3:-/path/to/source}"                                  # Rsync source module and path on remote (e.g. /chris/Documents) - module is set in rsyncd.conf

# Options
backupDepth=${backupDepth:-7}                                     # Number of backups to keep
timeout=${timeout:-1800}                                          # Timeout in seconds
interactiveMode="${interactiveMode:-no}"                          # Interactive use?

# Misc
dateCmd="${dateCmd:-date}"                                        # Current date
remoteSrc="${remote}${srcmodel}${srcpath}"                        # <remote>/<model>/<path>
src="${srcmodel}${srcpath}"
srcPathNoSlash="${2}"

# Define directories
BASE="/share/CACHEDEV1_DATA/backup/RSync"                         # Base location for backup on host
topLocalPath="${BASE}/${remote}${srcmodel}"                       # <BASE>/<remote>/<model>

# Define meta-data directory
ownFolderName="${ownFolderName:-.rsync-incremental-backup}"       # Rsync incremental backup directory name
ownFolderPath="${topLocalPath}/${ownFolderName}"                  # <BASE>/<remote>/<model>/.rsync-incremental-backup/

# Define meta-data files
exclusionFileName="${exclusionFileName:-exclude.txt}"             # File containing list of files to be excluded
exclusionFilePath="${ownFolderPath}/${exclusionFileName}"         # <BASE>/<remote>/<model>/.rsync-incremental-backup/exclude.txt

rotationLockFileName="${rotationLockFileName:-.rsync-rotation-lock}"  # Filename of rsync lock file
rotationLockFilePath="${ownFolderPath}/${rotationLockFileName}"       # <BASE>/<remote>/<model>/.rsync-incremental-backup/.rsync-rotation-lock

logFolderName="${logFolderName:-logs}"                            # Log folder name
logFolderPath="${ownFolderPath}/${logFolderName}"                 # <BASE>/<remote>/<model>/.rsync-incremental-backup/logs

logFileName="${logFileName:-RSync_backup_${remote}_${srcPathNoSlash}_$(${dateCmd} +%Y-%m-%d)_$(${dateCmd} +%H-%M-%S).log}" # Name of logfile
logFilePath="${logFolderPath}/${logFileName}"                     # <BASE>/<remote>/<model>/.rsync-incremental-backup/logs/<logname>

# Define folder filenames
partialFolderName="${partialFolderName:-.rsync-partial}"          # Name of folder for partial transfers
partialFolderPath="${ownFolderPath}/${partialFolderName}"         # <BASE>/<remote>/<model>/.rsync-incremental-backup/.rsync-partial


pathBak0="${pathBak0:-data}"                                      # <BASE>/<remote>/<model>/data
nameBakN="${nameBakN:-backup}"                                    # <BASE>/<remote>/<model>/backup.N

bak0="${topLocalPath}/${pathBak0}"

mkdir -p ${logFolderPath}
touch ${logFilePath}
touch ${exclusionFilePath}

writeToLog() {
	echo -e "${1}" | tee -a "${logFilePath}"
}

writeToLog "********************************"
writeToLog "*                              *"
writeToLog "*   rsync-incremental-backup   *"
writeToLog "*                              *"
writeToLog "********************************"

# Prepare backup paths
i=1
while [ "${i}" -le "${backupDepth}" ]
do
	export "bak${i}=${topLocalPath}/${nameBakN}.${i}"
	true "$((i = i + 1))"
done

writeToLog "\\n[$(${dateCmd} -Is)] You are going to backup"
writeToLog "\\tfrom:  ${remoteSrc}"
writeToLog "\\tto:    ${bak0}"

batchMode="yes"
if [ "${interactiveMode}" = "yes" ]
then
	batchMode="no"
fi

# Rotate backups if last rsync succeeded ..
if [ ! -d ${partialFolderPath} ] && [ ! -e ${rotationLockFilePath} ]
then
	# .. and there is previous data
	if [ -d ${bak0} ]
	then
		writeToLog "\\n[$(${dateCmd} -Is)] Backups rotation begins"

		true "$((i = i - 1))"

		# Remove the oldest backup if exists
		bak="bak${i}"
		rm -rf ${!bak}

		# Rotate the previous backups
		while [ "${i}" -gt 0 ]
		do
			bakNewPath="bak${i}"
			true "$((i = i - 1))"
			bakOldPath="bak${i}"
			if [ -d ${!bakOldPath} ]
			then
				mv ${!bakOldPath} ${!bakNewPath}
			fi
		done

		writeToLog "[$(${dateCmd} -Is)] Backups rotation finished\\n"
	else
		writeToLog "\\n[$(${dateCmd} -Is)] No previous data found, there are no backups to be rotated\\n"
	fi
else
	writeToLog "\\n[$(${dateCmd} -Is)] Last backup failed, backups will not be rotated\\n"
fi

# Set rotation lock file to detect in next run when backup fails

touch ${rotationLockFilePath}

writeToLog "[$(${dateCmd} -Is)] Backup begins\\n"

# Do the backup
if rsync -achvz --progress --timeout="${timeout}" --delete --no-W \
	--partial-dir="${partialFolderName}" --link-dest="${bak1}/" --log-file="${logFilePath}" --exclude="${ownFolderPath}" \
	--chmod=+r --exclude-from="${exclusionFilePath}" "rsync://${remoteSrc}/" "${bak0}/"
then
	writeToLog "\\n[$(${dateCmd} -Is)] Backup completed successfully\\n"

	# Clear unneeded partials and lock file
	rm -rf ${partialFolderPath} ${rotationLockFilePath}
	rsyncFail=0
else
	writeToLog "\\n[$(${dateCmd} -Is)] Backup failed, try again later\\n"
	rsyncFail=1
fi


exit "${rsyncFail}"

