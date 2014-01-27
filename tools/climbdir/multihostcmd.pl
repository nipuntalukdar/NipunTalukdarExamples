#!/usr/bin/perl
############################################################################
# A tool too execute command on multiple machines over SSH.
# Might be helpful if you want the same command to be executed on many machines
# 
# The tool is free, but I will appreciate if you send a mail to me if you are
# plannining to use it.
# I also request you to pay $1 to anyone in need if you are really using this
# script.
#
# Author: Nipun Talukdar
# EMail:  Nipun.Talukdar@gmail.com 
############################################################################

use threads (
    'yield',
    'stack_size' => 64 * 4096,
    'exit'       => 'threads_only',
    'stringify'
);
use Cwd qw(abs_path);
use Net::OpenSSH;

#
# executeCmdRemote
# executes the command on a remote host 
# command execution happens over ssh
#

sub executeCmdRemote {
    my ( $host, $command, @others ) = @_;
    my $ssh =  Net::OpenSSH->new($host,
         master_opts => [-o => "ConnectionAttempts=2", -o => "ConnectTimeout=5"] );
    if ($ssh->error) {
        return;
    }
    ($out, $err, @others) =  $ssh->capture2({timeout => 20}, $command);
    $outdata = "FROM $host ******************************************\n";
    if ($out ne "") {
        $outdata .= $out;
    }
    if ($err ne "") {
        $outdata .= $err;
    }
    $outdata .= "\nEND OF DATA FROM $host ************************************* \n\n";
    print $outdata;
}

#
# readHostFile
# reads from the file $HOME/.allhosts where this file contain a list of hosts
# each line on this file denotes a host name or host ip
# The given command is executed on this host
# 
sub readHostFile {
    my ($array, @others) = @_;
    $hostfile = $ENV{'HOME'} . '/.allhosts';
    if (! -e  $hostfile) {
        print $hostfile . ' doesn\'t exist';
        return;
    }
    if (! -f  $hostfile) {
        print $hostfile . ' is not a regular file';
        return;
    }
    open FH, "< $hostfile"  || return;
    @$array = <FH>;
    close FH;
}

sub main {
    if ( $#ARGV < 0 ) {
        $executing_script = abs_path($0);
        print "Usage: $executing_script command-to-execute\n";
        exit(1);
    }
    $cmdline = join( ' ', @ARGV );
    my @hostarry = ();
    readHostFile(\@hostarry);
    if ($#hostarry < 0) {
        print "Empty list for hosts";
        exit(1);
    }

    my $thr = undef;
    my @allthreads = ();
    foreach my $host (@hostarry) {
       $host =~ s/^\s+//;
       $host =~ s/\s+$//;
       if  ($host eq "") {
           next;
       }
       # Create a thread to execute the command on the remote host
       $thr = threads->create('executeCmdRemote', $host, $cmdline);
       push @allthreads, $thr;
    }
    foreach $thr (@allthreads){
        $thr->join();
    }
}

# Call main
main();
