from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import list2column

# Construct a BigQuery client object.
client = bigquery.Client()

class disease:
    def __init__(self, name):
        self.name = name
        self.df_chr = find_chr(self.name)
        self.df_gene = find_gene(self.df_chr['gene_id'])
        self.df_chr = concat_df(self.df_chr, self.df_gene)
        self.df_chr = define_information(self.df_chr)

def listed_diseases():
    query = "SELECT DISTINCT trait_reported FROM `thegwensproject.genomiX.disease_variant_gene` order by trait_reported;"
    query_job = client.query(query)  # Make an API request.
    df_diseases = query_job.to_dataframe()
    return df_diseases

def find_chr(disease):
    query = "SELECT DISTINCT lead_chrom, tag_chrom, gene_id, ancestry_initial, ancestry_replication FROM `thegwensproject.genomiX.disease_variant_gene` WHERE trait_reported = '" + disease + "' order by lead_chrom;"
    query_job = client.query(query)  # Make an API request.
    df_chr = query_job.to_dataframe()
    return df_chr

def find_gene(gene_id):
    query = "SELECT DISTINCT gene_name, gene_type, transcript_name, transcrypt_type, exon_number, exon_id, protein_id FROM `thegwensproject.gencode.annot` WHERE gene_id = '" + gene_id + "' order by lead_chrom;"
    query_job = client.query(query)  # Make an API request.
    df_gene = query_job.to_dataframe()
    return df_gene

def concat_df(df_chr, df_gene):
    #for each row of df_chr, find the corresponding gene_id in df_gene and add the gene_name, gene_type, transcript_name, transcrypt_type, exon_number, exon_id, protein_id to df_chr using the find gene function
    df_gene = find_gene(df_chr['gene_id'])
    df_chr = pd.concat([df_chr, df_gene], axis=1)
    return df_chr

def define_information(df_chr):
    #define per disease the percentage of specific ancestry origins from the ancestry_initial column knowing that the value of this column is a list type. each origin (european, african...) must be stored in a new column
    
    anc_init = list2column(df_chr, 'ancestry_initial')
    anc_repli = list2column(df_chr, 'ancestry_replication')

    df_chr = df_chr.drop(['ancestry_initial', 'ancestry_replication'], axis=1)
    number_genes_total = df_chr.shape[0]
    
    if df['col'].nunique() == 1:
        number_case = df['col'][0]
    else:
        number_case = df['col'].unique().sum()

