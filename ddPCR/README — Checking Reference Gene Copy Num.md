README — Checking Reference Gene Copy Number in Brachypodium distachyon Bd21-3 for ddPCR/qRT-PCR
This workflow counts how many loci in the Bd21-3 genome match three validated reference genes (UBC18, GAPDH, EF1α) using BLAST with explicit cutoffs. It’s designed for ddPCR/qRT-PCR assay design where effective copy number matters.

Genes and orthologs
We start from the three housekeeping genes validated in Brachypodium (paper: doi:10.1186/1471-2229-8-112). Use the Arabidopsis orthologs in that paper (Table 1) as anchors to pull Brachypodium orthologs in Phytozome (Bd21-3 v1.1/1.2), and to construct BLAST queries.

Gene	Arabidopsis ortholog	Notes
UBC18	At5g42990	Ubiquitin-conjugating enzyme
GAPDH (cytosolic)	At3g04120	Be careful not to mix plastid vs cytosolic isoforms
EF1α	At5g60390	Multigene family; uniqueness depends on primer placement

What this README gives you
Reproducible BLAST-based locus counting with explicit thresholds

Optional collapsing of exon-level HSPs into per-locus counts

Hooks to annotate hits with Bd21-3 gene IDs using the GFF3

Optional in-silico PCR step for assay-level uniqueness

Inputs
Genome: B. distachyon Bd21-3 genome FASTA and GFF3 (Phytozome Bd21-3 v1.1/1.2).

Queries: Arabidopsis genomic DNA sequences for the three orthologs (as requested).

(Recommended alternative: also prepare CDS or protein sequences for robustness.)

(Optional) Your ddPCR/qPCR primer sequences (FASTA or TSV).

Directory layout (suggested):

bash
Copy
Edit
project/
  data/
    genome/Bd21-3.fa
    genome/Bd21-3.gff3
    queries/arabidopsis_gDNA.fa        # contains At5g42990, At3g04120, At5g60390 gDNA
    queries/arabidopsis_protein.fa     # optional
  results/
  scripts/
Software
NCBI BLAST+ (2.12+)

bedtools (2.30+)

awk / coreutils

(Optional) seqkit, Primer-BLAST or an in-silico PCR tool

Parameters (cutoffs)
Per your specification:

E-value < 1e-10

Bit score > 90

Percent identity > 70%

These are applied to blastn HSPs (Arabidopsis gDNA → Bd21-3 genome).

You can set them as environment variables:

bash
Copy
Edit
export EVALUE=1e-10
export MINSCORE=90
export MINPID=70
Step 0 — Retrieve Bd21-3 orthologs (context check)
Use Phytozome (Bd21-3 v1.1/1.2) to look up orthologs of At5g42990, At3g04120, At5g60390. Keep these IDs handy to sanity-check your BLAST results (e.g., confirm cytosolic GAPDH, not plastid).

(This step is for verification; the BLAST steps below answer the copy-count directly.)

Step 1 — Build the BLAST database
bash
Copy
Edit
makeblastdb -in data/genome/Bd21-3.fa -dbtype nucl -out data/genome/Bd21-3
Step 2 — Run nucleotide BLAST (Arabidopsis gDNA → Bd21-3 genome)
Using a divergence-tolerant task:

bash
Copy
Edit
blastn -task dc-megablast \
  -query data/queries/arabidopsis_gDNA.fa \
  -db data/genome/Bd21-3 \
  -evalue $EVALUE \
  -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' \
  -num_threads 8 \
  > results/blastn_gDNA_vs_Bd21-3.tsv
Step 3 — Filter hits by your thresholds
bash
Copy
Edit
awk -v minp="$MINPID" -v mins="$MINSCORE" -v maxe="$EVALUE" 'BEGIN{FS=OFS="\t"} 
  ($13+0 <= maxe && $12+0 > mins && $3+0 > minp)' \
  results/blastn_gDNA_vs_Bd21-3.tsv \
  > results/blastn_gDNA_vs_Bd21-3.filtered.tsv
Columns (outfmt 6):
1 qseqid | 2 sseqid | 3 pident | 4 length | 5 mismatch | 6 gapopen | 7 qstart | 8 qend | 9 sstart | 10 send | 11 evalue | 12 bitscore

Step 4 — Collapse exon-level HSPs into genomic loci
A single gene often appears as multiple exon HSPs. Merge nearby HSPs per subject scaffold to count loci rather than exon fragments.

Convert to BED-like intervals (0-based, sorted), then merge within 5 kb:

bash
Copy
Edit
awk 'BEGIN{FS=OFS="\t"} {s=$9; e=$10; if(s>e){t=s;s=e;e=t} print $2, s-1, e, $1}' \
  results/blastn_gDNA_vs_Bd21-3.filtered.tsv \
  | sort -k1,1 -k2,2n \
  > results/blastn_gDNA_vs_Bd21-3.filtered.bed

bedtools merge -i results/blastn_gDNA_vs_Bd21-3.filtered.bed -d 5000 -c 4 -o distinct \
  > results/blastn_gDNA_vs_Bd21-3.loci.bed
results/blastn_gDNA_vs_Bd21-3.loci.bed now lists non-overlapping merged intervals representing putative loci hit by each query.

Count loci per gene (qseqid):

bash
Copy
Edit
# Map merged loci back to query IDs by overlapping the original HSPs (with qseqid in col4)
bedtools intersect -wa -wb \
  -a results/blastn_gDNA_vs_Bd21-3.loci.bed \
  -b results/blastn_gDNA_vs_Bd21-3.filtered.bed \
  > results/loci_with_qids.tsv

# Summarize unique loci per query
awk 'BEGIN{FS=OFS="\t"} {loc=$1":"$2"-"$3; q=$8} {print q,loc}' results/loci_with_qids.tsv \
  | sort -u | awk '{c[$1]++} END{for(k in c) print k,c[k]}' \
  > results/copy_counts_per_query.tsv
You’ll get a simple table like:

php-template
Copy
Edit
At5g42990   <N_loci>
At3g04120   <N_loci>
At5g60390   <N_loci>
These N_loci are the genomic copy counts that satisfy your thresholds.

(Optional) Step 5 — Attach Bd21-3 gene IDs
Annotate merged loci with the Bd21-3 GFF3 to see which genes were hit:

bash
Copy
Edit
# Convert loci bed to GFF3-ish for intersect
bedtools intersect -wa -wb \
  -a results/blastn_gDNA_vs_Bd21-3.loci.bed \
  -b data/genome/Bd21-3.gff3 \
  | awk 'BEGIN{FS=OFS="\t"} $10=="gene"{print $1,$2,$3,$13}' \
  > results/loci_to_geneIDs.tsv
You can then join loci_to_geneIDs.tsv with loci_with_qids.tsv to map qseqid → Bd21-3 gene IDs.

(Optional but recommended) Protein-level search
Because introns diverge, tblastn is often cleaner for ortholog discovery:

bash
Copy
Edit
tblastn -query data/queries/arabidopsis_protein.fa \
  -db data/genome/Bd21-3 \
  -evalue 1e-10 \
  -outfmt '6 qseqid sseqid pident length qstart qend sstart send evalue bitscore' \
  -num_threads 8 \
  > results/tblastn_protein_vs_Bd21-3.tsv
You may apply similar thresholds (e.g., E≤1e-10, bitscore>90, pident>50–60%) and the same locus-merging logic.

(Optional) Step 6 — Confirm assay-level uniqueness (in-silico PCR)
BLAST counts potential copies. ddPCR cares about what your primers amplify.
Run in-silico PCR/Primer-BLAST against Bd21-3 with your actual primers and:

Confirm a single amplicon at the expected size, or

Redesign primers if multiple amplicons are predicted.

(Tooling varies; document your command or web settings alongside the primer set.)

Interpreting results for ddPCR
If copy_counts_per_query.tsv shows 1 locus for a gene, treat it as single-copy (subject to in-silico PCR confirmation).

If >1 loci pass the BLAST thresholds, either choose a unique exon/junction to redesign primers, or acknowledge multi-copy normalization.

For absolute quantification, Bd21-3 genome size: ~309 Mb (1C ≈ 0.316 pg). A single-copy locus yields ≈ 6.3×10³ copies/ng of diploid gDNA (scale to your input).

Reproducibility notes
Record exact genome build (Bd21-3 v1.1 or v1.2), BLAST+ version, and the exact thresholds used.

Save raw and filtered BLAST tables under results/.

Commit your query FASTAs (or document accession versions and how they were exported).

Deliverables
results/blastn_gDNA_vs_Bd21-3.tsv — raw BLAST HSPs

results/blastn_gDNA_vs_Bd21-3.filtered.tsv — filtered by E<1e-10, bitscore>90, pident>70%

results/blastn_gDNA_vs_Bd21-3.loci.bed — merged loci

results/copy_counts_per_query.tsv — copy counts per gene

(Optional) results/loci_to_geneIDs.tsv — Bd21-3 gene IDs per locus

(Optional) in-silico PCR report per primer set

The criterial is:
The cut off is aligned length >200 identity >= 70%  E value<1E-10