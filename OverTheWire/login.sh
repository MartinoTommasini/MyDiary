if test $# -ne 1;then
	echo "Usage: $0 <levelnumber>"
	exit 1
fi

ssh behemoth${1}@behemoth.labs.overthewire.org -p 2221
