#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;

#by Li Lei 05-03-2022 in Berkeley 
#This script is to split the peptide fasta file into S and D subgenomes;
#usage:

my ($file1,$file2, $file3) = @ARGV;
my %hash;
open(TXT, "$file1") or die "Could not open $file1";
open(OUT1, ">$file2") or die "Could not open $file2";
open(OUT2, ">$file3") or die "Could not open $file3";

my %id2seq1 = ();#Bsyl
my $seqid;
#read in the DNA string using the fasta subfunction
while(<TXT>){
        chomp;
        if($_ =~ /^>(.+)/){
              $seqid = $1;         
        }else{
            $id2seq1{$seqid} .= $_;
        }
}
close(TXT);

foreach my $key (keys %id2seq1){
        #print "$key\n";
        if ($key =~ /^Pavir\.(\d+)K/ ){
                print OUT1 ">$key\n";
                print OUT1 "$id2seq1{$key}\n";
        }
        elsif($key =~ /^Pavir\.(\d+)N/){
                print  OUT2 ">$key\n";
                print  OUT2  "$id2seq1{$key}\n";
        }
}
close(OUT1);
close(OUT2);