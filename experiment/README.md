# Materials, data, and analysis code for the paper "Maze made easy: Better and easier measurement of incremental processing difficulty".

Note: This study is a replication and comparision with Witzel et al. 2012. The experimental sentences, half the comprehension questions, and the G- and L-maze distractors all come from Witzel et al. 2012. Additionally, all data/conditions described as "lab" come from their experiment.

## Materials: 
This folder has source for running the experiment in ibex. Copy header, material, and footer sections together into a .js file to go in data_includes part of an ibex experiment. (This uses the Maze and Maze_separator modules described in ibex_maze)
 - header.js: top part of file for Maze tasks (comment out G-maze part and uncomment L-maze part to show L-maze instructions)
 - footer.js: bottom part of file for Maze tasks
 - header_spr.js: top part of file for SPR
 - footer_spr.js: bottom part of file for SPR
 - g_maze.js: materials for G-maze 
 - l_maze.js: materials for L-maze
 - spr.js: materials for SPR
 - gulordava.js: materials for Gulordava A-maze 
 - one_b.js: materials for Jocefowicz A-maze
 
## Labelled: 
This folder contains the sentences labelled by critical word location, used to add labels to results during analysis.
 
## Data: 
This folder contains our data files.
 - Raw: data files produced from ibex (tsv format, lines starting with # are comments, see ibex documentation for more details; README in ibex_maze may be useful for maze specific results)
 - Processed: .rds files produced by read_Results.R from raw data; data is tidy and rectangular.

## Witzel:
This folder contains data from Witzel et al. 2012. 
 - .txt data files are their raw data files
 - .txt materials files are used to associate data with materials when parsing
 - .rds files are processed versions made by parse_witzel_data.R 
 
## Code:
This folder contains R code for parsing results into tidy data format and R code for all analyses and graphs in the paper. 
 - read_Results.R: takes raw files, tidies the data into .rds files (for our data)
 - parse_witzel_data.R: takes raw data, tidies the data into .rds files (for Witzel data)
 - Results.Rmd: runs regressions to determine estimated effect sizes, graph of effect sizes (note: models take time to run)
 - errors.Rmd: makes graphs of participants errors, can be used to view by item error rates
 - power.Rmd: does power analysis (note: models take a lot of time to run)
 
 
 
 

 
 
