library(GENESPACE)
runwd <- file.path("~/Projects/LDRD/Switchgrass/genome/Genespace")
gids <- c("K_Pvirgatum","N_Pvirgatum")

library(GENESPACE)
genomeRepo <- "~/Projects/LDRD/Switchgrass/genome/Genespace/rawGenomes/"
wd <- "~/Projects/LDRD/Switchgrass/genome/Genespace"
path2mcscanx <- "~/softwares/MCScanX"

#genomes2run <- c("Oropetium","Osativa", "Bsylv","Bstacei","Bdist","Barb","Sitalica","Sviridis","Sbicolor")
genomes2run <- c("K_Pvirgatum","N_Pvirgatum")

parsedPaths <- parse_annotations(
  rawGenomeRepo = genomeRepo,
  genomeDirs = genomes2run,
  genomeIDs = genomes2run,
  presets = "phytozome",
  genespaceWd = wd)

gpar <- init_genespace(
  wd = wd,
  path2mcscanx = path2mcscanx)

out <- run_genespace(gpar, overwrite = T)

ripd <- plot_riparian(
  gsParam = out,
  refGenome = "K_Pvirgatum", 
  useRegions = FALSE)

#hits <- read_allBlast(
 # filepath = file.path(out$paths$syntenicHits, 
                       "mouse_vs_human.allBlast.txt.gz"))
#ggdotplot(hits = hits, type = "all", verbose = FALSE)
