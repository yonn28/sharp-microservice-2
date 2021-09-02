from flask import Flask, jsonify, request
import pandas as pd
from urllib.request import urlopen
import joblib
import ssl
import json
import functions

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)

#-----------------------------------------Models and DataBases-------------------------

##-----------*Relapse*----------------
with urlopen('https://storage.googleapis.com/ds4all-test-bd1/Modelo_relapse.sav') as response:
   modelo_relapse = joblib.load(response)

base_relapse = pd.read_csv('https://storage.googleapis.com/ds4all-test-bd1/base_relapse.csv').drop(["IdBeneficiario","Unnamed: 0"],axis=1)

#-----------------------------------------Top 10 df-------------------------

#-----------------------------------------*Relapse*------------------------------
top10_df_r = functions.createTable_top(modelo_relapse, base_relapse)
p_range_r = str(top10_df_r["Range_probability"].iloc[0])
n_children_r = top10_df_r.shape[0]
shap_r = functions.plotShapValuesTop(modelo_relapse, top10_df_r)
s_table_r = functions.table_to_show(top10_df_r)
show_table_r = s_table_r[s_table_r['AVG ZScore'] > -100]
rows_r = show_table_r.shape[0]

"""

"""

@app.route('/api/v2/rel_n', methods=['GET'])
def getting_dataframe_rel_n():
    return jsonify(n_children_r)

@app.route('/api/v2/rel_p', methods=['GET'])
def getting_dataframe_rel_p():
    return jsonify(p_range_r)

@app.route('/api/v2/shap_rel', methods=['GET'])
def getting_dataframe_shap_rel():
    return jsonify(shap_r)

@app.route('/api/v2/rows_rel', methods=['GET'])
def getting_dataframe_rows_rel():
    return jsonify(rows_r)

@app.route('/api/v2/show_rel', methods=['GET'])
def getting_dataframe_rel():
    initial = int(request.headers.get('initial'))
    end = int(request.headers.get('end'))
    return jsonify(show_table_r[initial:end].to_dict("records"))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) #change port to 8080 for deployment, and host = '0.0.0.0'
    # app.run(debug=True, port=3000) #change port to 8080 for deployment, and host = '0.0.0.0'0