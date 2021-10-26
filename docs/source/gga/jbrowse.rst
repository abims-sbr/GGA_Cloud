Deploy JBrowse
==============

Rename the datasets you will use in JBrowse (gff, ...) to something more readable. These names will appear in the final JBrowse as track names.

For JBrowse, the next step is to use the tool Visualisation>JBrowse genome browse. Select the genome and the tracks you want, with all needed settings (including the contextual menus linking to Tripal pages), then Execute.

Parameters:

* Reference genome to display: Use a genome from history

* Select the reference genome: Fasta file

* Genetic code: The Standard code

* JBrowse-in-Galaxy Action: New JBrowse Instance

* Create as many track group as needed (examples: Annotation, Alignements, RNASeq, Misc, ...)

* In each track group, add 1 track per input file (gff, bam, ...)

* For GFF annotation tracks, enable Index this track. Disable it for repeated elements as it's useless + itslows down everythign (too many names to index)

* For GFF, choose:
	* JBrowse Track Type [Advanced]: Neat HTML Features
	* JBrowse Styling Options [Advanced], JBrowse style.className: transcript

* To add a contextual menu pointing to Tripal pages, add a JBrowse Contextual Menu options item, with:
	* Menu label: View transcript report
	* Menu title: Transcript {id}
	* Menu url: https://your_host/sp/genus_species/feature/Genus/species/mRNA/{id}


Note: in some cases, if the menu url is wrong, you can write more complicated things in Menu url, like:

.. code-block:: bash

  function(track,feature,div) { return 'https://your_host/sp/genus_species/feature/Genus/species/mRNA/'+feature.children()[0].get('id')}

Once finished, you can preview the JBrowse instance inside Galaxy (Eye icon). If it's ok, the next step is to push it into production.

Use the Visualisation>Add organisms to JBrowse container will replace any existing organism tool.

Parameters:

* JBrowse HTML Output: The jbrowse you just created
* Display name: Genus species
* Advanced>Unique ID: gspecies (the same as defined in docker-compose.yml, for ENABLE_JBROWSE of tripal container)

In case of multiple variants of a same organism, you can add several JBrowse datasets in this form.
Once you click on Execute, your JBrowse will be transfered to the JBrowse container, replacing any existing organism.