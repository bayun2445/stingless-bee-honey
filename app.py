from flask import request, jsonify, Flask
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import json
import logging
import joblib
import os

from helper import wavelength_xlsx_to_array

app = Flask(__name__)

# import model
# svm_file = open('./model/model_svm_stingless_bee_honey.pkl','rb')
svm_file = open('./model/model_svm_prob.pkl','rb')
pca_file = open('./model/pca.pkl', 'rb')
model = joblib.load(svm_file)
pca = joblib.load(pca_file)

# logs
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# folder simpan file
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return ("Flask app deployed!")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            water_content = request.form['water_content']
            diastase = request.form['diastase']
            hmf = request.form['hmf']
            reducing_sugar = request.form['reducing_sugar']
            saccharose = request.form['saccharose']
            acidity = request.form['acidity']

            # handle file upload
            uploaded_file = request.files['wavelength_file']
            file_save_path = os.path.join(UPLOAD_FOLDER, secure_filename(uploaded_file.filename))
            uploaded_file.save(file_save_path)

            # preprocess data
            features = [water_content,diastase,hmf,reducing_sugar,saccharose,acidity]
            wavelength = wavelength_xlsx_to_array(file_save_path)
            raw_input = np.concatenate([features, wavelength])
            input_columns = ['WaterContent','Diastase','Hydroxymethylfurfural','Reducing Sugar','Saccharose','Acidity',357,357.5,358,358.5,359,359.5,360,360.5,361,361.5,362,362.5,363,363.5,364,364.5,365,365.5,366,366.5,367,367.5,368,368.5,369,369.5,370,370.5,371,371.5,372,372.5,373,373.5,374,374.5,375,375.5,376,376.5,377,377.5,378,378.5,379,379.5,380,380.5,381,381.5,382,382.5,383,383.5,384,384.5,385,385.5,386,386.5,387,387.5,388,388.5,389,389.5,390,390.5,391,391.5,392,392.5,393,393.5,394,394.5,395,395.5,396,396.5,397,397.5,398,398.5,399,399.5,400,400.5,401,401.5,402,402.5,403,403.5,404,404.5,405,405.5,406,406.5,407,407.5,408,408.5,409,409.5,410,410.5,411,411.5,412,412.5,413,413.5,414,414.5,415,415.5,416,416.5,417,417.5,418,418.5,419,419.5,420,420.5,421,421.5,422,422.5,423,423.5,424,424.5,425,425.5,426,426.5,427,427.5,428,428.5,429,429.5,430,430.5,431,431.5,432,432.5,433,433.5,434,434.5,435,435.5,436,436.5,437,437.5,438,438.5,439,439.5,440,440.5,441,441.5,442,442.5,443,443.5,444,444.5,445,445.5,446,446.5,447,447.5,448,448.5,449,449.5,450,450.5,451,451.5,452,452.5,453,453.5,454,454.5,455,455.5,456,456.5,457,457.5,458,458.5,459,459.5,460,460.5,461,461.5,462,462.5,463,463.5,464,464.5,465,465.5,466,466.5,467,467.5,468,468.5,469,469.5,470,470.5,471,471.5,472,472.5,473,473.5,474,474.5,475,475.5,476,476.5,477,477.5,478,478.5,479,479.5,480,480.5,481,481.5,482,482.5,483,483.5,484,484.5,485,485.5,486,486.5,487,487.5,488,488.5,489,489.5,490,490.5,491,491.5,492,492.5,493,493.5,494,494.5,495,495.5,496,496.5,497,497.5,498,498.5,499,499.5,500,500.5,501,501.5,502,502.5,503,503.5,504,504.5,505,505.5,506,506.5,507,507.5,508,508.5,509,509.5,510,510.5,511,511.5,512,512.5,513,513.5,514,514.5,515,515.5,516,516.5,517,517.5,518,518.5,519,519.5,520,520.5,521,521.5,522,522.5,523,523.5,524,524.5,525,525.5,526,526.5,527,527.5,528,528.5,529,529.5,530,530.5,531,531.5,532,532.5,533,533.5,534,534.5,535,535.5,536,536.5,537,537.5,538,538.5,539,539.5,540,540.5,541,541.5,542,542.5,543,543.5,544,544.5,545,545.5,546,546.5,547,547.5,548,548.5,549,549.5,550,550.5,551,551.5,552,552.5,553,553.5,554,554.5,555,555.5,556,556.5,557,557.5,558,558.5,559,559.5,560,560.5,561,561.5,562,562.5,563,563.5,564,564.5,565,565.5,566,566.5,567,567.5,568,568.5,569,569.5,570,570.5,571,571.5,572,572.5,573,573.5,574,574.5,575,575.5,576,576.5,577,577.5,578,578.5,579,579.5,580,580.5,581,581.5,582,582.5,583,583.5,584,584.5,585,585.5,586,586.5,587,587.5,588,588.5,589,589.5,590,590.5,591,591.5,592,592.5,593,593.5,594,594.5,595,595.5,596,596.5,597,597.5,598,598.5,599,599.5,600,600.5,601,601.5,602,602.5,603,603.5,604,604.5,605,605.5,606,606.5,607,607.5,608,608.5,609,609.5,610,610.5,611,611.5,612,612.5,613,613.5,614,614.5,615,615.5,616,616.5,617,617.5,618,618.5,619,619.5,620,620.5,621,621.5,622,622.5,623,623.5,624,624.5,625,625.5,626,626.5,627,627.5,628,628.5,629,629.5,630,630.5,631,631.5,632,632.5,633,633.5,634,634.5,635,635.5,636,636.5,637,637.5,638,638.5,639,639.5,640,640.5,641,641.5,642,642.5,643,643.5,644,644.5,645,645.5,646,646.5,647,647.5,648,648.5,649,649.5,650,650.5,651,651.5,652,652.5,653,653.5,654,654.5,655,655.5,656,656.5,657,657.5,658,658.5,659,659.5,660,660.5,661,661.5,662,662.5,663,663.5,664,664.5,665,665.5,666,666.5,667,667.5,668,668.5,669,669.5,670,670.5,671,671.5,672,672.5,673,673.5,674,674.5,675,675.5,676,676.5,677,677.5,678,678.5,679,679.5,680,680.5,681,681.5,682,682.5,683,683.5,684,684.5,685,685.5,686,686.5,687,687.5,688,688.5,689,689.5,690,690.5,691,691.5,692,692.5,693,693.5,694,694.5,695,695.5,696,696.5,697,697.5,698,698.5,699,699.5,700,700.5,701,701.5,702,702.5,703,703.5,704,704.5,705,705.5,706,706.5,707,707.5,708,708.5,709,709.5,710,710.5,711,711.5,712,712.5,713,713.5,714,714.5,715,715.5,716,716.5,717,717.5,718,718.5,719,719.5,720,720.5,721,721.5,722,722.5,723,723.5,724,724.5,725,725.5]
            df_input_features = pd.DataFrame(raw_input, index=input_columns)
            df_input_features.index = df_input_features.index.astype(str)
            input_pca = pca.transform(df_input_features.transpose())  
            
            # prediksi
            df_new_data_input = pd.DataFrame(input_pca, columns=['comp 1', 'comp 2', 'comp 3', 'comp 4', 'comp 5', 'comp 6'])  
            prediction = model.predict_proba(df_new_data_input)
            prediction_probabilities = prediction.tolist()[0]
            label = int(np.argmax(prediction))

            return jsonify({
                'success': True,
                'message': 'Prediction success!',
                'result': {
                    'label_num': label,
                    'accuracy': 0.9625,
                    'label_prob': prediction_probabilities[label]
                }
            }), 200

        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Error: Invalid input data',
                'result': {
                    'label_num': None, 
                    'accuracy': None,
                    'label_prob': None
                }
            }), 400

        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Error: {e}',
                'result': {
                    'label_num': None, 
                    'accuracy': None,
                    'label_prob': None
                }
            }), 500

@app.route('/spectral-data', methods=['GET'])
def getSpectralData():
    try:
        with open('./asset/spectral_data_imputed.json', 'r') as file:
            data = json.load(file)    

        return jsonify({
            'success': True,
            'error': None,
            'data': data,
        }), 200

    except FileNotFoundError:
        return jsonify({
            'success': False,
            'error': 'File not found',
            'data': None
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error: {e}',
            'data': None
        }), 500

if __name__ == '__main__':
    app.run(debug=True)