#!/usr/bin/perl
use strict;
use Getopt::Long;
use Net::SSH::Expect;
use Data::Dumper;
use Log::Log4perl;

# logfile configuration
Log::Log4perl->init("log.conf");

# command line data
my %client = (
	'ip' => '',
	'user' => '',
	'password' => '',
);
my $help = 0;

# getopts configuration
my %GetOptionsHash = (
	"client_ip=s" => \$client{ip},
	"client_user=s"   => \$client{user},
	"client_password=s"  => \$client{password},
	"help"	=> \$help,
);
GetOptions(%GetOptionsHash) or die("Error in command line arguments\n");

# command line data validation
if($help == 1 || $client{ip} == '' || $client{user} == '' || $client{password} == '') {
	&display_help_info();
	exit(0);
}



# displays help information
sub display_help_info() {
	my $log = Log::Log4perl->get_logger("main");
	$log->info("Displaying help information below");
	my $help_info = "
USAGE:
	--client_ip			IP address of the client machine to be configured for
					SSH Authentication (Current computer is SSH server)
	--client_user			Username for SSH login on the client machine (for
					adding the authentication files to the client machine)
	--client_password		SSH password for the given client machine username
	--help				Prints this help message
";
	print $help_info;
}
