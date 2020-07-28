#!/usr/bin/env python

from __future__ import print_function

import argparse
import collections
import json
import logging as log
import os
import sys

from shutil import copyfile
from subprocess import call


class BlastBank:

    def __init__(self, raw_org, data_dir_root, rel_path, fasta_file_name, db_dir_root, seq_type, path, is_multi):
        self.raw_org = raw_org
        self.org = prettify(raw_org)
        self.data_dir_root = data_dir_root
        self.rel_path = rel_path
        self.fasta_file_name = fasta_file_name
        self.db_dir_root = db_dir_root
        self.seq_type = seq_type
        self.path = path  # http://bipaa.genouest.org/sp/xxx/ Can be the same as raw_org, or something else when having multiple genomes.
        self.is_multi = is_multi

        self.fasta = os.path.join(data_dir_root, rel_path, fasta_file_name)
        self.dest_path = os.path.splitext(os.path.join(db_dir_root, self.path, rel_path, fasta_file_name))[0]
        self.title = sanitize(rel_path + '_' + os.path.splitext(self.fasta_file_name)[0])
        if self.is_multi:
            fake_path = rel_path.split('/')
            if len(fake_path) > 2:
                fake_path = [fake_path[1]] + [fake_path[0]] + fake_path[2:]
            fake_path = '/'.join(fake_path)
            self.pretty_name = prettify(fake_path, True)
        else:
            self.pretty_name = self.org + ' ' + prettify(rel_path, False)

        with open(self.fasta, 'r') as f:
            self.first_id = f.readline()[1:].rstrip()

        if self.seq_type == 'nucl':
            if 'transcript' in self.fasta_file_name.lower() or 'cdna' in self.fasta_file_name.lower():
                self.pretty_name += " transcripts"
            elif 'cds' in self.fasta_file_name.lower():
                self.pretty_name += " CDS"
        else:
            if 'protein' in self.fasta_file_name.lower() or 'pep' in self.fasta_file_name.lower() or 'proteome' in self.fasta_file_name.lower() or self.fasta_file_name.endswith('.faa'):
                self.pretty_name += " proteins"

        # Just a stupid/hacky string used for sorting bank list
        self.sort_key = 'a_' if 'genome' in self.title else 'b_'
        self.sort_key += self.pretty_name

    def __str__(self):
        return str({
            'raw_org': self.raw_org,
            'org': self.org,
            'data_dir_root': self.data_dir_root,
            'rel_path': self.rel_path,
            'fasta_file_name': self.fasta_file_name,
            'db_dir_root': self.db_dir_root,
            'seq_type': self.seq_type,
            'path': self.path,
            'fasta': self.fasta,
            'dest_path': self.dest_path,
            'title': self.title,
            'pretty_name': self.pretty_name,
        })


def main(args):

    genome_path = os.path.basename(os.getcwd())
    if not args.multi_org:
        genome_name = genome_path
    data_dir_root = os.path.abspath(os.path.join('src_data'))
    if not os.path.isdir(data_dir_root):
        raise Exception("Could not find data dir: %s" % data_dir_root)

    db_dir_root = os.path.abspath(args.dest)

    ignore_list = ['func_annot', "apollo_source"]
    if args.ignore:
        ignore_list += args.ignore

    # Looking for files
    log.info("Looking for fasta files in %s:" % data_dir_root)
    banks = []
    for root, dirs, files in os.walk(data_dir_root, followlinks=True):
        file_list = [os.path.realpath(os.path.join(root, filename)) for filename in files]
        rel_path = root[len(data_dir_root) + 1:]

        skip_current = False
        for ign in ignore_list:
            if ign in rel_path:
                skip_current = True

        if not skip_current:  # skip useless data
            for f in file_list:
                f = os.path.basename(f)
                if f.endswith('.fasta') or f.endswith('.fa') or f.endswith('.fna') or f.endswith('.faa'):
                    if args.multi_org:
                        genome_name = rel_path.split('/')[1]

                    if 'protein' in f or 'pep.' in f or 'proteome' in f or f.endswith('.faa'):
                        seq_type = 'prot'
                    else:
                        seq_type = 'nucl'
                    new_bank = BlastBank(genome_name, data_dir_root, rel_path, f, db_dir_root, seq_type, genome_path, args.multi_org)
                    log.info("Found '%s' of type: %s" % (new_bank.fasta, new_bank.seq_type))
                    banks.append(new_bank)

    if not banks:
        log.info("No fasta file found.")
    else:
        for b in banks:
            makeblastdb(b, args.dry_run, args.no_parse_seqids)

    nuc_list = collections.OrderedDict()
    prot_list = collections.OrderedDict()
    banks.sort(key=lambda x: x.sort_key)
    for b in banks:
        if b.seq_type == 'nucl':
            if b.pretty_name not in nuc_list:
                nuc_list[b.dest_path] = b.pretty_name
            else:
                nuc_list[b.dest_path] = "%s (%s)" % (b.pretty_name, b.fasta_file_name)
        else:
            if b.pretty_name not in prot_list:
                prot_list[b.dest_path] = b.pretty_name
            else:
                prot_list[b.dest_path] = "%s (%s)" % (b.pretty_name, b.fasta_file_name)

    yml_dir = os.path.abspath('blast')
    yml_file_path = os.path.abspath(os.path.join(yml_dir, 'banks.yml'))
    links_file_path = os.path.abspath(os.path.join(yml_dir, 'links.yml'))
    if not args.dry_run:

        log.info("List of bank names (to use in links.yml):")
        write_titles(banks)

        log.info("Writing bank list in '%s'" % yml_file_path)
        if not os.path.exists(yml_dir):
            os.makedirs(yml_dir, mode=0o755)
        yml_file = open(yml_file_path, 'w')
        write_yml(yml_file, nuc_list, prot_list)

        log.info("Writing automatic links to links.yml in '%s'" % links_file_path)
        if os.path.exists(links_file_path):
            log.info("Making backup of previous links.yml to '%s'" % (links_file_path + '.back'))
            copyfile(links_file_path, links_file_path + '.back')
        links_yml_file = open(links_file_path, 'w')
        write_links_yml(links_yml_file, banks, args.apollo)

    else:
        log.info("List of bank names (to use in links.yml):")
        write_titles(banks)
        log.info("Would write bank list in '%s'" % yml_file_path)
        write_yml(sys.stdout, nuc_list, prot_list)
        log.info("Would write links.yml in '%s'" % links_file_path)
        write_links_yml(sys.stdout, banks, args.apollo)


def write_yml(yml_file, nuc_list, prot_list):

    nuc = "~"
    prot = "~"

    if nuc_list:
        nuc = "\n                ".join(['%s: %s' % (json.dumps(k), json.dumps(v)) for k, v in nuc_list.items()])
    if prot_list:
        prot = "\n                ".join(['%s: %s' % (json.dumps(k), json.dumps(v)) for k, v in prot_list.items()])

    print("genouest_blast:", file=yml_file)
    print("    db_provider:", file=yml_file)
    print("        list:", file=yml_file)
    print("            nucleic:", file=yml_file)
    print("                %s" % nuc, file=yml_file)
    print("            proteic:", file=yml_file)
    print("                %s" % prot, file=yml_file)


def write_links_yml(yml_file, banks, apollo):

    for bank in banks:
        print("", file=yml_file)
        print("# %s" % (bank.pretty_name), file=yml_file)

        link = ''
        if bank.seq_type == 'prot':
            spl = bank.org.split()
            if len(spl) > 2:
                sp_str = '/'.join(spl[:2])
                sp_str += '-' + '-'.join(spl[2:])
            else:
                sp_str = '/'.join(spl)
            link = 'http://abims-gga.sb-roscoff.fr/sp/%s/feature/%s/polypeptide/{id}' % (bank.path, sp_str)
        elif 'genome' in bank.title:
            dataset_id = bank.org.lower()
            spl = dataset_id.split()
            if len(spl) == 2:  # Genus species => gspecies
                dataset_id = spl[0][:1] + spl[1]
            elif len(spl) == 3:  # Genus species strain1 => gsstrain1
                dataset_id = spl[0][:1] + spl[1][:1] + spl[2]
            else:  # Genus species some garbage => genus_species_some_garbage
                dataset_id = dataset_id.replace(' ', '_')
            if apollo:
                link = '<a href="http://abims-gga.sb-roscoff.fr/sp/' + bank.path + '/jbrowse/?data=data%2F' + dataset_id + '&loc={id}{jbrowse_track}">{id}</a> <a href="http://abims-gga.sb-roscoff.fr/sp/' + bank.path + '/apollo/annotator/loadLink?loc={id}:1{apollo_track}">Apollo</a>'
            else:
                link = '<a href="http://abims-gga.sb-roscoff.fr/sp/' + bank.path + '/jbrowse/?data=data%2F' + dataset_id + '&loc={id}{jbrowse_track}">{id}</a>'
        else:
            spl = bank.org.split()
            if len(spl) > 2:
                sp_str = '/'.join(spl[:2])
                sp_str += '-' + '-'.join(spl[2:])
            else:
                sp_str = '/'.join(spl)
            link = 'http://abims-gga.sb-roscoff.fr/sp/%s/feature/%s/mRNA/{id}' % (bank.path, sp_str)

        if link:
            print("%s:" % (bank.title), file=yml_file)
            print("    db: '%s'" % (bank.title), file=yml_file)
            print("    '*': '%s'" % (link), file=yml_file)
        else:
            print("# Skipped", file=yml_file)


def write_titles(banks):

    for bank in banks:
        print("'%s' -> '%s'      [%s]" % (bank.pretty_name, bank.title, bank.first_id))


def makeblastdb(bank, dry_run, no_parse_seqids):
    log.info("Formatting bank: %s  --->  %s" % (bank.fasta, bank.dest_path))
    dest_dir = os.path.realpath(os.path.join(bank.dest_path, '..'))
    if not os.path.exists(dest_dir):
        log.info("Creating folder: %s" % dest_dir)
        if not dry_run:
            os.makedirs(dest_dir, mode=0o755)
    parse = "-parse_seqids"
    if no_parse_seqids:
        parse = ""
    cmd = "makeblastdb -in '%s' -dbtype '%s' %s -out '%s' -title '%s'" % (bank.fasta, bank.seq_type, parse, bank.dest_path, bank.title)
    log.info("Running: %s" % cmd)
    if not dry_run:
        try:
            retcode = call(cmd, shell=True)
            if retcode != 0:
                raise RuntimeError("Child was terminated by signal " + str(retcode))
        except OSError as e:
            print("Execution failed:" + e, file=sys.stderr)
            sys.exit(1)


def prettify(name, capital=True):
    name = name.replace('_', ' ')
    name = name.replace('/', ' ')
    if capital:
        name = name[0].upper() + name[1:]

    return name


def sanitize(name):
    name = name.lower()
    name = name.replace(' ', '_')
    name = name.replace('/', '_')

    return name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate blast databanks and update blast forms.'
    )
    parser.add_argument("-v", "--verbose", help="Increase output verbosity.",
                        action="store_true")
    parser.add_argument("-d", "--dry-run", help="Dry run: no modification will be done, for testing purpose.",
                        action="store_true")
    parser.add_argument("-m", "--multi-org", help="Add this flag if there are multiple organisms in src_data.",
                        action="store_true")
    parser.add_argument("-a", "--apollo", help="Add this flag to generate links to apollo.",
                        action="store_true")
    parser.add_argument("-p", "--no-parse-seqids", help="Don't use the makeblastdb -parse_seqids option (use this in case you have strange looking sequence ids that make html files unreadable)",
                        action="store_true")
    parser.add_argument("--ignore", help='Files or directories to ignore', nargs='*')
    parser.add_argument("dest", help="Destination directory (not including the genome name, should be mounted on compute nodes)")

    args = parser.parse_args()
    log.basicConfig(level=log.INFO)
    if args.verbose:
        log.basicConfig(level=log.DEBUG)

    main(args)
