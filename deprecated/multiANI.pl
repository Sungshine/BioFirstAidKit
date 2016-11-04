#!/usr/bin/perl -w
###Run ANI on a dataset in command line
use strict;
my $start_run = time();
my @files = <*.fasta>;

#nested for loop to compare each element to all
my @ani;
for (my $i=0; $i < @files; $i++){
	$ani[$i][$i] = 100;
    for (my $j=$i+1; $j < @files; $j++){
        print STDERR "Computing ANI between $files[$i] and $files[$j]\n";
        my $ani = `perl ANIb.pl -bl blastall -fd formatdb -qr $files[$i] -sb $files[$j] -od result`;
        chomp $ani;
        $ani[$i][$j] = $ani;
        $ani[$j][$i] = $ani;
    }
}
print "\n";

for (my $i=0; $i < @files; $i++){
	my $file = $files[$i];
	$file =~ s/\.fasta//;
	print "\t$file";
}
for (my $i=0; $i < @files; $i++){
	my $file = $files[$i];
	$file =~ s/\.fasta//;
	print "\n$file";
    for (my $j=0; $j < @files; $j++){
        print "\t$ani[$i][$j]";
    }
}

my $end_run = time();
print STDERR "Complete job took: ".($end_run - $start_run)." sec\n";