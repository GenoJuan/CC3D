#!/usr/bin/perl;

# El programa requiere rutas absolutas

use strict;

my $path_to_cc3d_software = "/Users/ewiggin/CC3D_3.7.5/";

my $path_to_cc3d   = $ARGV[0];
my $combs  = $ARGV[2];
my $rep    = $ARGV[3];

my %parms_values = ();
my %parms_files;

my $parm  = ();
my $value = ();
my @values = ();
my $file  = ();

open(parms, $ARGV[1]);

while(<parms>){
    if(/(.+) (.+) (.+)/){
        $parm  = $1;
        $value = $2;
        $file  = $3;
        
        @values = split(',', $value);
        
        $parms_values{$parm} = [@values];
        $parms_files{$parm}  = $file;
        
        
    }
    
} close(parms);

foreach $parm (keys(%parms_values)){
    print "$parm\t@{$parms_values{$parm}}\t$parms_files{$parm}\n";
}

my @combinations = split(':', $combs);
my $number_of_combs = scalar(@combinations);

print "@combinations\n";

print "Performing parameter scan for $number_of_combs combinations of parameters\n";

for(my $c = 0; $c < scalar(@combinations); $c++){
    &parameter_scan($combinations[$c], 0, "", "")
    
}







########################################################################################################
#########################################     Sub-routines     #########################################
########################################################################################################

# Input
# parameters_to_test: parm1,parm2,parm3
# position. Por default 0
# parameters ""
# values 00

sub parameter_scan{
    my $parameters_to_test = $_[0];
    my $pos = $_[1];
    my $parameters = $_[2];
    my $values = $_[3];
    
    my @parameters = split(',', $parameters_to_test);
    
    for(my $value = 0; $value < scalar(@{$parms_values{$parameters[$pos]}}); $value++){
        if($pos <= (scalar(@parameters) - 2)){
            &parameter_scan($parameters_to_test, $pos + 1, $parameters . $parameters[$pos] . "-", $values . "${$parms_values{$parameters[$pos]}}[$value]" . "-");
        }
        else{
            my $params = $parameters . $parameters[$pos];
            my $val = $values . "${$parms_values{$parameters[$pos]}}[$value]";
            &modify_files($params, $val);
            

        }
        
    }
}

########################################################################################################


# Input:
# a) $params_to_scan is a character string containing the names of the parameters to scan in the format:
# "param1-param2-param3" as returned by the sub-routine "parameter_scan".
# b) $values_to_scan is a character string containing the values of the paramters to scan in the format:
# "value1-value2-value" as returned by the sub-routine "parameter_scan". Where value1 is the assigned to the param1 and so on.
# In addition the sub-routine uses the global variables "$path_to_cc3d" and "%parms_files".

sub modify_files{
    my $params_to_scan = $_[0];
    my $values_to_scan = $_[1];
    
    my @params_to_scan = split('-', $params_to_scan);
    my @values_to_scan = split('-', $values_to_scan);
    
    my $path_to_cc3d_copy = $path_to_cc3d . '_temp';
    system("cp -r $path_to_cc3d $path_to_cc3d_copy");
    
    for(my $p = 0; $p < scalar(@params_to_scan); $p++){
        my $path_to_file = $path_to_cc3d_copy . "/Simulation/" . $parms_files{$params_to_scan[$p]};
        
        if($path_to_file =~ /.py/){
            if($path_to_file =~ /Steppables.py/){
                my $from = "\(.*= )[0-9]*[\.\|e+\|e-]*[0-9]*\(.*\)### ParameterScan:$params_to_scan[$p]";
                my $to   = "\\1$values_to_scan[$p]\\2### ParameterScan:$params_to_scan[$p]";
        
                system("sed -i '' -E 's/$from/$to/' $path_to_file");
            
            } else {
                my $from = "\(.*\"\)[0-9]*[\.\|e+\|e-]*[0-9]*\(\".*\)### ParameterScan:$params_to_scan[$p]\|\(.*frequency=\)[0-9]*\(.*\)### ParameterScan:$params_to_scan[$p]";
                my $to   = "\\1\\3$values_to_scan[$p]\\2\\4### ParameterScan:$params_to_scan[$p]";
        
                system("sed -i '' -E 's/$from/$to/' $path_to_file");
            }
        }
        if($path_to_file =~ /.xml/){
              print "hola\n";
              my $from = "\(.*>)[0-9]*[\.\|e+\|e-]*[0-9]*\(<.*\)<!-- ParameterScan:$params_to_scan[$p] -->";
              my $to   = "\\1$values_to_scan[$p]\\2<!-- ParameterScan:$params_to_scan[$p] -->";
              
              system("sed -i '' -E 's/$from/$to/' $path_to_file");
        }
    }
    
    &run_simulation($path_to_cc3d_copy);
    
    
    system("rm -r $path_to_cc3d_copy");
    
}

########################################################################################################

# Input:
# directory: a character string specifying the absolute path to the directory where the *.cc3d file is stored.
# In addition the sub-routine also uses the global variable "$rep" to indicate the number of repetions to perform.

sub run_simulation{
    my $directory = $_[0];
    my $repetitions = $rep;
   
    for(my $r = 0; $r < $repetitions; $r++){
        my $command = $path_to_cc3d_software . "runScript.command -i " . $directory . "\/\*\.cc3d";
        system("$command");
    }
}