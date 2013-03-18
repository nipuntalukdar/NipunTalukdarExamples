######################################################################
# This is a bash function for climbing up directories by
# certtain level.
# Save it in a file named testup.sh
# Then source it as $ source testup.sh
# After that you will be able to climb up directories by issuing
# below command
# $ up <number-of-level-up>   
# E.g. up 7
#
# Written for the fedup world by Nipun (Nipun.talukdar@gmail.com)
# God bless all
#
#####################################################################


function up {
    if [ $# -lt 1 ] ; then
        return 0
    fi
    i=1
    updir=""

    while [ $i -le $1 ] ; do
        i=`expr $i + 1`
        if [ -z "$updir" ] ; then
            updir=..
        else 
            updir=${updir}/..
        fi
        if [ $? -ne 0 ] ; then 
            return $?
        fi
    done
    cd $updir
    return $?
}
