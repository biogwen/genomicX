from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()


class DiseaseForm(FlaskForm):
    lead_chromosome = StringField('Lead Chromosome', validators=[DataRequired()])
    lead_position = StringField('Lead Position', validators=[DataRequired()])
    tag_chromosome = StringField('Tag Chromosome', validators=[DataRequired()])
    tag_position = StringField('Tag Position', validators=[DataRequired()])
    disease = StringField('Disease', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate(self):
        # First call the original validation
        valid = super().validate()

        # Count the number of empty fields
        empty_fields = sum(
            1 for field in [self.lead_chromosome, self.lead_position, self.tag_chromosome, self.tag_position, self.disease]
            if not field.data
        )

        # If at least 4 fields are empty, add an error to the form
        if empty_fields >= 4:
            self.lead_chromosome.errors.append("At least two fields must be filled!")
            valid = False

        return valid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def home():
    form = DiseaseForm()
    table = ''
    if form.validate_on_submit():
        lead_chromosome = form.lead_chromosome.data or "0"
        lead_position = form.lead_position.data or "0"
        tag_chromosome = form.tag_chromosome.data or "0"
        tag_position = form.tag_position.data or "0"
        disease = form.disease.data or "0"
        # call the information function
        df = information(lead_chromosome, lead_position, tag_chromosome, tag_position, disease)

        # convert the DataFrame to HTML
        table = df.to_html()
        # you can now use these variables in your application

    diseases = list_diseases()  # assuming this function returns a DataFrame
    disease_list = diseases['trait_reported'].unique().tolist()
    return render_template('home.html', form=form, disease_list=disease_list)

def list_diseases():
    query = "SELECT DISTINCT trait_reported FROM `thegwensproject.genomiX.disease_variant_gene` order by trait_reported;"
    query_job = client.query(query)  # Make an API request.
    return query_job.to_dataframe()

def information(lead_chromosome, lead_position, tag_chromosome, tag_position, disease):
    query = "SELECT * FROM thegwensproject.genomiX.variant_disease_gene WHERE "

    # Add conditions to the query if the form input is not "0"
    conditions = []
    if lead_chromosome != "0":
        conditions.append(f"lead_chrom = '{lead_chromosome}'")
    if lead_position != "0":
        conditions.append(f"lead_pos = {int(lead_position)}")
    if tag_chromosome != "0":
        conditions.append(f"tag_chrom = '{tag_chromosome}'")
    if tag_position != "0":
        conditions.append(f"tag_pos = {int(tag_position)}")
    if disease != "0":
        conditions.append(f"trait_reported = '{disease}'")

    # Join all conditions with AND
    query += " AND ".join(conditions)
    query_job = client.query(query)  # Make an API request.
    return query_job.to_dataframe()
    # Now you can run the query and return the result
    # Here I'll just return the query itself for demonstration
    
    
    
def variant_disease(lead_chromosome, lead_position, tag_chromosome, tag_position, disease):
    query = "SELECT * FROM thegwensproject.genomiX.variant_disease WHERE "

    # Add conditions to the query if the form input is not "0"
    conditions = []
    if lead_chromosome != "0":
        conditions.append(f"lead_chrom = '{lead_chromosome}'")
    if lead_position != "0":
        conditions.append(f"lead_pos = {int(lead_position)}")
    if tag_chromosome != "0":
        conditions.append(f"tag_chrom = '{tag_chromosome}'")
    if tag_position != "0":
        conditions.append(f"tag_pos = {int(tag_position)}")
    if disease != "0":
        conditions.append(f"trait_reported = '{disease}'")

    # Join all conditions with AND
    query += " AND ".join(conditions)
    query_job = client.query(query)  # Make an API request.
    return query_job.to_dataframe()


if __name__ == '__main__':
    app.run(debug=True)