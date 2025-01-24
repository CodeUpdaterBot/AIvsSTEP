import requests
import re
from openai import OpenAI
import os

# Below is an example of how you could store questions 1–50 in a Python list of dictionaries.
# Each entry includes:
#   question_number: The question index (1 to 50).
#   question: The full text of the question stem.
#   choices: A dictionary of the multiple-choice options.
#   correct_answer: The letter of the correct answer.

practice_test_questions = [
    {
        "question_number": 1,
        "question": (
            "A 14-year-old boy is brought to the emergency department by his parents because of a 1-month "
            "history of intermittent right knee pain that has worsened during the past day. He rates his "
            "current pain as a 6 on a 10-point scale and says that it worsens when he walks and lessens "
            "when he sits. During the past 2 weeks, he has been walking 1 mile daily in preparation for "
            "participation in the school marching band. He has not taken any medications for his pain. "
            "He sustained a right tibia and fibula fracture at the age of 8 years after a skateboarding "
            "accident, which was treated with internal fixation and casting. He has asthma treated with "
            "inhaled budesonide daily and inhaled albuterol as needed. His mother has type 2 diabetes "
            "mellitus, and his maternal grandmother has osteoporosis. The patient is 170 cm (5 ft 7 in; 77th "
            "percentile) tall and weighs 88 kg (195 lb; >95th percentile); BMI is 31 kg/m2 (98th percentile). "
            "Temperature is 37.0°C (98.6°F), pulse is 95/min, and blood pressure is 130/80 mm Hg. Physical "
            "examination shows hyperpigmented, thickened skin at the nape of the neck. There is tenderness "
            "to palpation of the anterior aspect of the right hip and limited range of motion on abduction, "
            "internal rotation, and flexion of the right hip. The left hip and knees are nontender; range "
            "of motion is full in all directions. The remainder of the examination discloses no "
            "abnormalities. Which of the following factors in this patient’s history most increased his "
            "risk for developing this condition?"
        ),
        "choices": {
            "A": "BMI",
            "B": "Family history",
            "C": "Medication use",
            "D": "Previous fractures",
            "E": "Recent physical activity",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 2,
        "question": (
            "A 14-year-old girl is brought to the office by her mother because of a 3-month history of red "
            "bumps on her skin. The patient says the bumps are not itchy or painful but that she finds them "
            "embarrassing. She has no history of major medical illness and takes no medications. Her vital "
            "signs are within normal limits. Physical examination shows the findings in the photograph. "
            "Which of the following is the most likely diagnosis?"
        ),
        "choices": {
            "A": "Eczema",
            "B": "Folliculitis",
            "C": "Hidradenitis",
            "D": "Keratosis pilaris",
            "E": "Urticaria",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 3,
        "question": (
            "A 50-year-old man comes to the office because of a 2-month history of increasing daytime "
            "somnolence. He has obstructive sleep apnea for which he has only intermittently used a "
            "continuous positive airway pressure device. He is 170 cm (5 ft 7 in) tall and weighs 181 kg "
            "(400 lb); BMI is 63 kg/m2. His temperature is 37°C (98.6°F), pulse is 100/min, respirations "
            "are 12/min, and blood pressure is 135/80 mm Hg. Physical examination shows a gray-blue tinge "
            "to the lips, earlobes, and nail beds. Cardiac examination shows no other abnormalities. Arterial "
            "blood gas analysis on room air shows a pH of 7.31, PCO2 of 70 mm Hg, and PO2 of 50 mm Hg. "
            "Which of the following additional findings would be most likely in this patient?"
        ),
        "choices": {
            "A": "Decreased serum bicarbonate concentration",
            "B": "Increased hemoglobin concentration",
            "C": "Increased total lung capacity",
            "D": "Left ventricular hypertrophy",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 4,
        "question": (
            "A 32-year-old man comes to the office because of a 1-day history of cough productive of small "
            "amounts of blood and a 2-day history of shortness of breath and swelling of his ankles. He also "
            "has a 2-week history of progressive fatigue and episodes of dark urine. He has no history of "
            "major medical illness and takes no medications. His temperature is 37°C (98.6°F), pulse is "
            "90/min, respirations are 18/min, and blood pressure is 175/110 mm Hg. Pulse oximetry on room "
            "air shows an oxygen saturation of 91%. Diffuse inspiratory crackles are heard over all lung "
            "bases. There is 2+ pitting edema of both ankles. Results of laboratory studies are shown:\n\n"
            "Hemoglobin 8.9 g/dL\nHematocrit 27%\n\nSerum\nUrea nitrogen 55 mg/dL\nCreatinine 2.9 mg/dL\n\n"
            "Urine RBC 20–40/hpf\nUrinalysis also shows some dysmorphic RBCs and rare RBC casts.\n"
            "Examination of a kidney biopsy specimen shows crescentic glomerulonephritis and linear "
            "deposition of IgG along the glomerular capillaries. This patient most likely has antibodies "
            "directed against which of the following antigens?"
        ),
        "choices": {
            "A": "Collagen",
            "B": "Double-stranded DNA",
            "C": "Nucleolar protein",
            "D": "Phospholipid",
            "E": "Proteins in neutrophil cytoplasm",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 5,
        "question": (
            "A 5-year-old girl is brought to the emergency department because of a 2-day history of fever, "
            "urinary urgency, and burning pain with urination. She has had four similar episodes during the "
            "past year. A diagnosis of urinary tract infection is made. Subsequent renal ultrasonography "
            "shows one large U-shaped kidney. Which of the following is the most likely embryologic origin "
            "of this patient's condition?"
        ),
        "choices": {
            "A": "Failure of the kidneys to rotate 90 degrees medially",
            "B": "Failure of normal kidney ascent",
            "C": "Failure of one ureteric bud to develop normally",
            "D": "Fusion of the inferior poles of the metanephros during ascent",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 6,
        "question": (
            "A 78-year-old man comes to the office for a follow-up examination. He was discharged from the "
            "hospital 1 week ago after being treated for a nontuberculous mycobacterial infection. He started "
            "treatment with ciprofloxacin and rifampin at that time. He also has hypertension and underwent "
            "placement of a mechanical aortic valve 6 years ago for aortic stenosis. Other current medications "
            "are hydrochlorothiazide, lisinopril, and warfarin. His warfarin dose was doubled 4 days ago. "
            'He says that he is trying to follow a healthier diet. He drinks two 12-oz beers daily. Results of '
            "laboratory studies done 4 days ago and today are shown:\n\n"
            "4 Days Ago      Today\n"
            "Prothrombin time  11 sec (INR=1)    11.2 sec (INR=1.1)\n"
            "Partial thromboplastin time 29 sec  27 sec\n\n"
            "Which of the following is the most likely cause of this patient's laboratory findings?"
        ),
        "choices": {
            "A": "Decreased protein binding",
            "B": "Eradication of gut flora",
            "C": "Increased alcohol intake",
            "D": "Increased vegetable consumption",
            "E": "Induction of cytochrome enzymes",
        },
        "correct_answer": "E"
    },
    {
        "question_number": 7,
        "question": (
            "A 32-year-old man comes to the office because of a 2-week history of fever and throat pain. "
            "He is 173 cm (5 ft 8 in) tall and weighs 63 kg (140 lb); BMI is 21 kg/m2. His pulse is 110/min, "
            "respirations are 16/min, and blood pressure is 98/68 mm Hg. Physical examination shows scattered "
            "2- to 4-cm lymph nodes in the neck, axillae, and inguinal regions. There is a bilateral tonsillar "
            "exudate but no ulcerations. Results of laboratory studies are shown:\n\n"
            "Hemoglobin 9.6 g/dL\nHematocrit 29%\nLeukocyte count 1500/mm3\nPlatelet count 60,000/mm3\n\n"
            "A heterophile antibody test result is negative. Which of the following is the most likely "
            "diagnosis?"
        ),
        "choices": {
            "A": "Epstein-Barr virus infection",
            "B": "Gonococcal pharyngitis",
            "C": "HIV infection",
            "D": "Lymphogranuloma venereum infection",
            "E": "Streptococcal pharyngitis",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 8,
        "question": (
            "A 50-year-old man comes to the office for a follow-up examination. He has a 2-month history of "
            "headache and shortness of breath with exertion. He also has hypertension treated with "
            "hydrochlorothiazide for the past 2 years. His blood pressure is 180/105 mm Hg. Ophthalmoscopic "
            "examination is most likely to show which of the following in this patient?"
        ),
        "choices": {
            "A": "Arteriovenous nicking",
            "B": "Melanocytes in the uvea",
            "C": "Optic neuritis",
            "D": "Posterior subcapsular cataracts",
            "E": "Tractional retinal detachment",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 9,
        "question": (
            "A 65-year-old woman with a history of rheumatic mitral valve disease is brought to the emergency "
            "department 30 minutes after the sudden onset of right-sided weakness and inability to speak. "
            "Neurologic examination shows weakness of the right lower side of the face and difficulty "
            "swallowing. Muscle strength is 3/5 on the right side. She can understand what is said to her, "
            "but she cannot repeat words or answer questions. An ECG shows atrial fibrillation. The most "
            "likely cause of the neurologic findings in this patient is occlusion of which of the following "
            "labeled arteries in the photograph of a normal brain?"
        ),
        "choices": {
            "A": "A",
            "B": "B",
            "C": "C",
            "D": "D",
            "E": "E",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 10,
        "question": (
            "A 51-year-old man with a 10-year history of gastroesophageal reflux and suspected Barrett "
            'esophagus comes to the office because his omeprazole dose "doesn\'t work around the Christmas '
            'holidays." He states that he prides himself on having a large appetite and "holding his liquor" '
            "during the holidays. He currently takes the maximum dose of omeprazole. Which of the following "
            "is the most appropriate initial action by the physician?"
        ),
        "choices": {
            "A": "Ask the patient how much he is eating and drinking during the holidays",
            "B": "Explain the hazards of untreated reflux in the presence of Barrett esophagus",
            "C": "Order an upper endoscopy",
            "D": "Refer the patient to a gastroenterologist",
            "E": "Switch the omeprazole to pantoprazole",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 11,
        "question": (
            "A 60-year-old man comes to the office because of weakness, tingling of his hands and feet, "
            "irritability, and forgetfulness for 4 months. Physical examination shows pallor, weakness, "
            "and spasticity. Deep tendon reflexes are increased. Sensation to vibration is absent in the "
            "lower extremities. Laboratory studies show megaloblastic anemia, serum antiparietal cell "
            "antibodies, and increased serum concentrations of methylmalonic acid and total "
            "homocyst(e)ine. The synthesis of which of the following amino acids is most likely impaired "
            "in this patient?"
        ),
        "choices": {
            "A": "Cysteine",
            "B": "Glutamine",
            "C": "Methionine",
            "D": "Phenylalanine",
            "E": "Tyrosine",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 12,
        "question": (
            "A 65-year-old woman comes to the office for a follow-up examination 1 year after she underwent "
            "operative resection of the right colon and chemotherapy for stage III colon cancer. She reports "
            "fatigue. Physical examination shows no abnormalities. A staging CT scan of the chest and "
            "abdomen shows five new 2- to 3-cm masses in the liver and both lungs. This patient's cancer "
            "most likely spread to the lungs via which of the following structures?"
        ),
        "choices": {
            "A": "Inferior mesenteric vein",
            "B": "Inferior vena cava",
            "C": "Left colic vein",
            "D": "Middle colic artery",
            "E": "Pulmonary vein",
            "F": "Superior mesenteric artery",
            "G": "Superior vena cava",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 13,
        "question": (
            "A 26-year-old man comes to the office because of a 1-week history of increased urinary frequency "
            "accompanied by excessive thirst. He says he has been urinating hourly. Physical examination "
            "shows no abnormalities. Serum chemistry studies are within the reference ranges. Urine "
            "osmolality is 50 mOsmol/kg H2O. After administration of ADH (vasopressin), his urine osmolality "
            "is within the reference range. The most likely cause of this patient's symptoms is dysfunction "
            "of which of the following structures?"
        ),
        "choices": {
            "A": "Anterior pituitary gland",
            "B": "Bowman capsule",
            "C": "Glomerulus",
            "D": "Hypophysial portal system",
            "E": "Loop of Henle",
            "F": "Supraoptic nucleus",
        },
        "correct_answer": "F"
    },
    {
        "question_number": 14,
        "question": (
            "A 52-year-old woman comes to the office because of a 6-month history of intermittent headaches. "
            "Sometimes the pain improves when the patient lies down in a quiet room. Her temperature is "
            "37.5°C (99.5°F), pulse is 86/min, respirations are 16/min, and blood pressure is 154/100 mm Hg. "
            "The lungs are clear. Cardiac examination shows the point of maximal impulse displaced to the "
            "left and occasional skipped beats; there are no murmurs or rubs. There is no S3. Resting "
            "electrocardiography shows left axis deviation with R waves greater than 30 mm in leads V5 "
            "through V6. Which of the following processes best explains the development of the left "
            "ventricular abnormalities in this patient?"
        ),
        "choices": {
            "A": "Excessive accumulation of glycogen",
            "B": "Fibrosis of intraventricular conduction pathways",
            "C": "Increased synthesis of contractile filaments",
            "D": "Misfolding and aggregation of cytoskeletal proteins",
            "E": "Myocyte hyperplasia as a result of induction of embryonic genes",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 15,
        "question": (
            "A 53-year-old man comes to the physician because of a dry scaly rash on his body for the past "
            "year. He has had a 15-kg (33-lb) weight loss during the past year. He is 178 cm (5 ft 10 in) "
            "tall and now weighs 54 kg (120 lb); BMI is 17 kg/m2. His stools have a large volume and float. "
            "Which of the following nutrient deficiencies is most likely?"
        ),
        "choices": {
            "A": "Magnesium",
            "B": "Vitamin A",
            "C": "Vitamin B12 (cobalamin)",
            "D": "Vitamin C",
            "E": "Zinc",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 16,
        "question": (
            "Serum LDL-cholesterol concentrations are measured in blood samples collected from 25 healthy "
            "volunteers. The data follow a normal distribution. The mean and standard deviation for this "
            "group are 130 mg/dL and 25 mg/dL, respectively. The standard error of the mean is 5.0. With a "
            "95% confidence level, the true mean for the population from which this sample was drawn falls "
            "within which of the following ranges (in mg/dL)?"
        ),
        "choices": {
            "A": "105-155",
            "B": "120-140",
            "C": "125-135",
            "D": "128-132",
            "E": "129-131",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 17,
        "question": (
            "A 39-year-old man comes to the physician because of a 6-month history of progressive shortness "
            "of breath. He has had a cough productive of white sputum for 2 years. He smoked 1 pack of "
            "cigarettes daily for 16 years but quit 10 years ago. He is in mild respiratory distress with "
            "pursed lips and a barrel chest; he is using the accessory muscles of respiration. Breath sounds "
            "are distant and crackles are present in the lower lung fields bilaterally. Pulmonary function "
            "tests show a decreased FEV1:FVC ratio, increased residual volume, and decreased diffusion "
            "capacity. An x-ray of the chest shows hyperinflation and hypertranslucency of the lower lobes "
            "of both lungs. Which of the following is the most likely diagnosis?"
        ),
        "choices": {
            "A": "Asthma",
            "B": "Bronchiectasis",
            "C": "Chronic pulmonary fibrosis",
            "D": "Cystic fibrosis",
            "E": "Emphysema",
        },
        "correct_answer": "E"
    },
    {
        "question_number": 18,
        "question": (
            "Investigators conduct a study that evaluates the effect of finasteride on the incidence of "
            "prostate cancer in 500 patients. The investigators recruit an additional 1000 patients for the "
            "study. Which of the following effects will this have on the research study?"
        ),
        "choices": {
            "A": "Greater chance of a Type I error",
            "B": "Greater chance of a Type II error",
            "C": "Less chance of a Type I error",
            "D": "Less chance of a Type II error",
            "E": "Impossible to predict",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 19,
        "question": (
            "An 82-year-old woman has a 7-month history of increasing indigestion, upper abdominal bloating, "
            "and early satiety. Photomicrographs of her gastric wall are shown: A is a hematoxylin and eosin "
            "stain; B is a mucin stain; C is an immunostain for cytokeratin. Which of the following is "
            "most likely to have decreased expression in these cells?"
        ),
        "choices": {
            "A": "Cathepsin D",
            "B": "Epithelial cadherins",
            "C": "Heparin-binding fibroblast growth factors",
            "D": "Integrins",
            "E": "Type IV collagenase",
            "F": "Vascular endothelial growth factor",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 20,
        "question": (
            "A 54-year-old woman comes to the physician because she would like to lose weight. She has been "
            "on numerous diets in the past with limited success. Both her parents have type 2 diabetes "
            "mellitus. She is 160 cm (5 ft 3 in) tall and weighs 69 kg (152 lb); BMI is 27 kg/m2. Her blood "
            "pressure is 140/90 mm Hg. Fasting serum glucose concentration is 102 mg/dL. Compared with a "
            "woman of the same age whose weight is normal, which of the following serum abnormalities is "
            "most likely in this patient?"
        ),
        "choices": {
            "A": "Decreased cholesterol excretion",
            "B": "Decreased estrone concentration",
            "C": "Decreased leptin concentration",
            "D": "Increased fasting insulin concentration",
            "E": "Increased growth hormone concentration",
            "F": "Increased thyroid-stimulating hormone concentration",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 21,
        "question": (
            "A 65-year-old woman is brought to the emergency department because of a 10-minute history of "
            "chest tightness and severe pain of her left arm. Physical examination shows jugular venous "
            "distention. Crackles are heard over the lung fields. An ECG shows ST-segment elevation greater "
            "than 1 mm in leads V4 through V6 and new Q waves. Serum studies show an increased troponin I "
            "concentration. Which of the following labeled points in the graph best represents the changes "
            "in cardiac function that occurred during the first 10 seconds after the onset of pain in this "
            "patient?"
        ),
        "choices": {
            "A": "W → X",
            "B": "W → Y",
            "C": "W → Z",
            "D": "X → W",
            "E": "X → Y",
            "F": "X → Z",
            "G": "Z → W",
            "H": "Z → X",
            "I": "Z → Y",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 22,
        "question": (
            "A previously healthy 33-year-old woman is brought to the emergency department by the Secret "
            "Service for stalking the president of the USA for 2 months. She claims to be married to the "
            "president's twin brother and states that the president just had his twin kidnapped to avoid "
            "competition. She speaks rapidly and is difficult to interrupt. Her associations are often loose. "
            'She says, "I haven\'t slept for days, but I won\'t even try to sleep until my husband is rescued. '
            'God has been instructing me to take over the White House. I can\'t wait to be reunited with my '
            'husband. I hear his voice telling me what to do." When asked about drug use, she says she uses '
            'only natural substances. She refuses to permit blood or urine tests, saying, "I don\'t have time '
            'to wait for the results." Which of the following is the most likely diagnosis?'
        ),
        "choices": {
            "A": "Bipolar disorder, manic, with psychotic features",
            "B": "Brief psychotic disorder",
            "C": "Delusional disorder",
            "D": "Psychotic disorder due to general medical condition",
            "E": "Schizophrenia",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 23,
        "question": (
            "In informing a couple that their newborn has Down syndrome, there is a specific, relatively "
            "limited amount of information that the consulting physician should give immediately. The rest "
            "can be discussed at a later time. Which of the following best explains the purpose of using "
            "this approach to disclosure?"
        ),
        "choices": {
            "A": "Allowing the couple's primary care physician to discuss most of the information with them",
            "B": "Allowing the parents time to tell other family members",
            "C": "Delaying parental distress until the information is completely disclosed",
            "D": "Disclosing the most important information so that it can be understood as fully as possible",
            "E": "Influencing the parents' course of action about what is medically most appropriate",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 24,
        "question": (
            "A 62-year-old man comes to the physician because of a 6-month history of urinary hesitancy and "
            "dribbling after urination. He has to urinate two to three times nightly. Physical examination "
            "shows a diffusely enlarged, firm, and nontender prostate. Which of the following is most "
            "likely to have contributed to the development of this patient's condition?"
        ),
        "choices": {
            "A": "Activation of the α1-adrenergic receptor",
            "B": "Conversion of testosterone to dihydrotestosterone",
            "C": "Conversion of testosterone to estradiol",
            "D": "Inhibition of the α1-adrenergic receptor",
            "E": "Production of prostate-specific antigen",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 25,
        "question": (
            "A 19-year-old man who is in the US Army is brought to the emergency department 45 minutes "
            "after he sustained a knife wound to the right side of his chest during an altercation. He has "
            "no history of major medical illness and takes no medications. His temperature is 36.9°C (98.4°F), "
            "pulse is 110/min, respirations are 24/min, and blood pressure is 114/76 mm Hg. Pulse oximetry "
            "on room air shows an oxygen saturation of 94%. On physical examination, the trachea appears to "
            "be shifted to the left. Pulmonary examination of the right chest is most likely to show which "
            "of the following findings?"
        ),
        "choices": {
            "A": "Decreased fremitus, dull percussion, decreased breath sounds",
            "B": "Decreased fremitus, hyperresonant percussion, decreased breath sounds",
            "C": "Decreased fremitus, hyperresonant percussion, dull breath sounds",
            "D": "Increased fremitus, dull percussion, bronchial breath sounds",
            "E": "Increased fremitus, dull percussion, decreased breath sounds",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 26,
        "question": (
            "A 34-year-old man comes to the office because of a 1-month history of diarrhea. He has a history "
            "of pheochromocytoma treated 2 years ago. His mother is being treated for a tumor of her "
            "parathyroid gland. He has no other history of major medical illness and takes no medications. "
            "His temperature is 37.0°C (98.6°F), pulse is 84/min, respirations are 10/min, and blood "
            "pressure is 120/75 mm Hg. Pulse oximetry on room air shows an oxygen saturation of 97%. Vital "
            "signs are within normal limits. Physical examination shows a 3-cm, palpable mass on the right "
            "side of the neck. A biopsy specimen of the mass shows a neuroendocrine neoplasm of "
            "parafollicular cell origin. The most likely cause of the findings in this patient is a "
            "mutation in which of the following types of genes?"
        ),
        "choices": {
            "A": "Cell cycle regulation gene",
            "B": "DNA mismatch repair gene",
            "C": "Metastasis suppressor gene",
            "D": "Proto-oncogene",
            "E": "Tumor suppressor gene",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 27,
        "question": (
            "A 56-year-old man is brought to the emergency department by his wife 30 minutes after he had "
            "severe upper back pain and hoarseness before becoming comatose. He has hypertension treated "
            "with hydrochlorothiazide. His temperature is 37°C (98.6°F), pulse is 100/min, and blood "
            "pressure is 160/80 mm Hg in the right arm and 100/60 mm Hg in the left arm. Ophthalmologic "
            "examination shows ptosis and miosis of the left eye. There is anhidrosis of the left side of "
            "the forehead, right hemiplegia, and a decreased left radial pulse. A chest x-ray shows a "
            "widened mediastinum. Which of the following conditions is the most likely cause of these "
            "findings?"
        ),
        "choices": {
            "A": "Dissection of the aorta distal to the left subclavian artery",
            "B": "Dissection of the aorta extending into the left carotid artery",
            "C": "Dissection of the aorta extending into the left carotid artery and distal aortic arch",
            "D": "Dissection of the proximal aorta extending into the right subclavian artery",
            "E": "Superior sulcus tumor",
            "F": "Thrombus of the left carotid artery",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 28,
        "question": (
            "A 68-year-old man with alcohol use disorder comes to the office because of a 3-month history of "
            "intermittent blood in his urine; he has had no pain. He is a retired laboratory technician "
            "from a company that produces naphthylamine. He has smoked 1½ packs of cigarettes daily for 45 "
            "years. A CT scan of the abdomen shows a mass in the pelvis of the left kidney. A photograph "
            "of the surgically resected kidney is shown. The neoplastic process in this kidney is most "
            "likely to be which of the following?"
        ),
        "choices": {
            "A": "Angiomyolipoma",
            "B": "Metastatic melanoma",
            "C": "Nephroblastoma",
            "D": "Oncocytoma",
            "E": "Urothelial carcinoma",
        },
        "correct_answer": "E"
    },
    {
        "question_number": 29,
        "question": (
            "A 27-year-old woman comes to the emergency department because of a 1-hour history of severe "
            "shortness of breath. She has just returned from a cross-country flight. She has a history of "
            "borderline hypertension. Her temperature is 36.9°C (98.5°F), pulse is 113/min, respirations "
            "are 28/min, and blood pressure is 138/85 mm Hg. Physical examination shows that the right "
            "calf has an increased circumference compared with the left calf, and there is tenderness "
            "behind the right knee. Which of the following is the most likely underlying cause of this "
            "patient's condition?"
        ),
        "choices": {
            "A": "Antithrombin III deficiency",
            "B": "Factor V Leiden mutation",
            "C": "Glanzmann thrombasthenia",
            "D": "Protein C deficiency",
            "E": "von Willebrand disease",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 30,
        "question": (
            "A 20-year-old woman is brought to the urgent care center because of a 2-month history of "
            "progressive weakness of her arms. She also has a 1-week history of moderate back pain and "
            "headache. Her only medication is ibuprofen as needed for pain. Muscle strength is 3/5 in the "
            "upper extremities. Sensation to pinprick is decreased over the upper extremities. MRI of the "
            "spine shows a central syrinx in the cervical spinal cord. It is most appropriate to obtain "
            "specific additional history regarding which of the following in this patient?"
        ),
        "choices": {
            "A": "Diet",
            "B": "Family illness",
            "C": "Recent travel",
            "D": "Trauma",
            "E": "Unintended weight loss",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 31,
        "question": (
            "A 3-year-old boy is brought to the office because of a 2-day history of bulging of his left "
            "eye. He says his eye hurts. He has no history of major medical illness or recent trauma to "
            "the area, and he receives no medications. Vital signs are within normal limits. Physical "
            "examination shows exophthalmos of the left eye. MRI of the brain shows a 2-cm mass involving "
            "the ocular muscles of the left eye. A biopsy specimen of the mass shows malignant cells, some "
            "of which have striations. Which of the following is the most likely diagnosis?"
        ),
        "choices": {
            "A": "Neuroblastoma",
            "B": "Pheochromocytoma",
            "C": "Retinoblastoma",
            "D": "Rhabdomyosarcoma",
            "E": "Thyroid cancer",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 32,
        "question": (
            "An 18-year-old woman with sickle cell disease is brought to the emergency department by her "
            "parents because of a 2-hour history of severe abdominal pain and nausea. Her parents say that "
            "she had a cheeseburger, milk shake, and chocolate bar for lunch. Her temperature is 37°C "
            "(98.6°F). Physical examination shows tenderness over the right upper quadrant of the abdomen, "
            "radiating to the right shoulder. Ultrasonography of the right upper quadrant of the abdomen "
            "shows gallstones. Which of the following is the most likely underlying cause of this patient's "
            "current condition?"
        ),
        "choices": {
            "A": "Decreased hepatic secretion of lecithin",
            "B": "Decreased reabsorption of bile salts",
            "C": "High ratio of cholesterol to bile acids in bile",
            "D": "Infestation with parasites secreting β-glucuronidase",
            "E": "Overload of unconjugated bilirubin",
        },
        "correct_answer": "E"
    },
    {
        "question_number": 33,
        "question": (
            "In a sample of 100 individuals, the mean leukocyte count is 7500/mm3, with a standard deviation "
            "of 1000/mm3. If the leukocyte counts in this population follow a normal (gaussian) distribution, "
            "approximately 50% of individuals will have which of the following total leukocyte counts?"
        ),
        "choices": {
            "A": "5500–9500/mm3",
            "B": "<6500/mm3 or >8500/mm3",
            "C": "6500–8500/mm3",
            "D": "<7500/mm3",
            "E": ">9500/mm3",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 34,
        "question": (
            "A previously healthy 52-year-old woman comes to the physician because of a 2-month history of "
            "fatigue, constipation, and frequent urination. Her temperature is 37.1°C (98.8°F), pulse is "
            "80/min, respirations are 14/min, and blood pressure is 140/90 mm Hg. Diffuse crackles are heard "
            "bilaterally. Her serum calcium concentration is 11.1 mg/dL, and serum parathyroid hormone "
            "concentration is decreased. A chest x-ray shows bilateral hilar lymphadenopathy and interstitial "
            "infiltrates. Which of the following is the most likely cause of this patient's hypercalcemia?"
        ),
        "choices": {
            "A": "Calcitriol production by activated macrophages",
            "B": "Local resorption of bone by metastases",
            "C": "Parathyroid hormone-related peptide secretion",
            "D": "Secretion of parathyroid hormone",
            "E": "Secretion of thyroid-stimulating hormone",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 35,
        "question": (
            "A 55-year-old woman comes to the clinic because of a 2-month history of increasingly severe "
            "vaginal pain and itching during sexual intercourse. She avoids intercourse with her husband "
            "because of the symptoms. She has been in a monogamous relationship with her husband for the "
            "past 25 years. She has type 2 diabetes mellitus. Her vital signs are within normal limits. "
            "Pelvic examination shows edematous and erythematous vaginal mucosa with white discharge. A "
            "photomicrograph of a vaginal smear is shown. Which of the following is the most likely causal "
            "infectious agent?"
        ),
        "choices": {
            "A": "Candida albicans",
            "B": "Chlamydia trachomatis",
            "C": "Herpes simplex virus",
            "D": "Human papillomavirus",
            "E": "Trichomonas vaginalis",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 36,
        "question": (
            "A 24-year-old woman is brought to the physician 1 month after she was involved in a motor vehicle "
            "collision that left her weak and unable to walk. Physical examination shows weakness of both "
            "hands and atrophy of the intrinsic hand muscles bilaterally. There is weakness and increased "
            "muscle tone of the lower extremities on passive range of motion. Deep tendon reflexes are "
            "normal at the biceps and triceps bilaterally and are increased at the knees and ankles. "
            "Babinski sign is present bilaterally. Sensation to pinprick is absent at and below the level "
            "of the clavicles. The lesion in this patient is most likely located at which of the following "
            "spinal cord levels?"
        ),
        "choices": {
            "A": "C5",
            "B": "C7",
            "C": "T1",
            "D": "T3",
            "E": "T5",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 37,
        "question": (
            "A 45-year-old man is brought to the emergency department 30 minutes after the sudden onset of "
            "crushing chest pain. His father, maternal aunt, and paternal uncle all died of myocardial "
            "infarctions under the age of 50 years. Physical examination shows tendinous xanthomas on the "
            "hands and thickened Achilles tendons. Serum lipid studies show a total cholesterol "
            "concentration of 410 mg/dL, HDL-cholesterol concentration of 30 mg/dL, and triglyceride "
            "concentration of 140 mg/dL. The diagnosis of myocardial infarction is made. This patient most "
            "likely has a deficiency of which of the following?"
        ),
        "choices": {
            "A": "Apo B48",
            "B": "Apo C",
            "C": "HMG-CoA reductase activity",
            "D": "LDL receptor",
            "E": "Lipoprotein lipase activity",
        },
        "correct_answer": "D"
    },
    {
        "question_number": 38,
        "question": (
            "A previously healthy 19-year-old man is brought to the emergency department 30 minutes after he "
            "collapsed while playing softball. He had severe, sharp, upper back pain prior to the game. He "
            "is 196 cm (6 ft 5 in) tall. His temperature is 37°C (98.6°F), pulse is 130/min, respirations "
            "are 24/min, and blood pressure is 80/50 mm Hg. Physical examination shows pallor and no jugular "
            "venous distention. Breath sounds are clear. The carotid pulses are weak. A grade 4/6, late "
            "diastolic murmur is heard at the lower left sternal border. Which of the following is the most "
            "likely cause of this patient's cardiac findings?"
        ),
        "choices": {
            "A": "Atrial septal defect",
            "B": "Mitral stenosis",
            "C": "Papillary muscle rupture",
            "D": "Perforated tricuspid valve",
            "E": "Stretched aortic anulus",
        },
        "correct_answer": "E"
    },
    {
        "question_number": 39,
        "question": (
            "A 27-year-old woman is brought to the emergency department because of a 2-week history of "
            "double vision. Neurologic examination shows that the left eye does not adduct past the midline "
            "on horizontal gaze when the patient looks to the right. Leftward horizontal gaze is normal. "
            "This patient's ocular movement deficit is most likely caused by damage to which of the "
            "following structures?"
        ),
        "choices": {
            "A": "Left abducens nerve",
            "B": "Left medial longitudinal fasciculus",
            "C": "Left nucleus of the abducens nerve",
            "D": "Right abducens nerve",
            "E": "Right medial longitudinal fasciculus",
            "F": "Right nucleus of the abducens nerve",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 40,
        "question": (
            "A 45-year-old woman is recovering from acute respiratory distress syndrome secondary to gallstone "
            "pancreatitis. A drawing of the alveolar wall is shown. Which of the following labeled cells "
            "will most likely proliferate and reestablish the injured epithelial layer in this patient?"
        ),
        # This question references a figure with labeled cells (A, B, C, D, etc.),
        # but the final official answer is "D" from the key.
        "choices": {
            "A": "Type I pneumocyte (for example)",
            "B": "Another labeled cell, etc.",
            "C": "Another labeled cell, etc.",
            "D": "Type II pneumocyte (progenitor role)",
            # etc., hypothetical placeholders since the figure is not visible here.
        },
        "correct_answer": "D"
    },
    {
        "question_number": 41,
        "question": (
            "An 11-year-old girl is brought to the emergency department by her parents because of a 1-week "
            "history of breast enlargement. She has not had pain or nipple discharge. She has asthma treated "
            "with inhaled albuterol as needed. She does not smoke cigarettes, drink alcoholic beverages, or "
            "use illicit drugs. She is at the 50th percentile for height and weight. Vital signs are within "
            "normal limits. Examination of the breasts shows minimal enlargement under the areolae and "
            "mild enlargement of the diameter of the areolae without nipple discharge; no masses are "
            "palpated. There is scant pubic hair. Which of the following best describes the sexual maturity "
            "rating for this patient?"
        ),
        "choices": {
            "A": "1",
            "B": "2",
            "C": "3",
            "D": "4",
            "E": "5",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 42,
        "question": (
            "A 5-year-old boy is brought to the emergency department by his mother because of an episode of "
            "bloody stool 3 hours ago. The mother says the stool was hard 'like pebbles' and she noted "
            "bright red blood on the tissue when the patient cleaned himself. His previous bowel movement "
            "was 5 days ago. The patient has no abdominal or rectal pain now, but he did have abdominal "
            "pain during his bowel movement 5 days ago. He has no history of major medical illness and "
            "receives no medications. Vaccinations are up-to-date. The patient has no recent history of "
            "travel. He is at the 5th percentile for height and the 10th percentile for weight; BMI is at "
            "the 50th percentile. Vital signs are within normal limits. Abdominal examination shows "
            "hypoactive bowel sounds and a soft, slightly distended abdomen that is not tender to palpation. "
            "Rectal examination shows 1 cm of bright red rectal mucosa protruding from the right side of "
            "the anus; there is no rectal bleeding. The remainder of the examination shows no abnormalities. "
            "Which of the following is the most likely cause of this patient's physical findings?"
        ),
        "choices": {
            "A": "Constipation",
            "B": "Cystic fibrosis",
            "C": "Hirschsprung disease",
            "D": "Hookworm infestation",
            "E": "Intussusception",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 43,
        "question": (
            "A 25-year-old woman comes to the office because of a 3-day history of fever, chills, severe "
            "headache, weakness, muscle pain, loss of appetite, vomiting, diarrhea, and moderate abdominal "
            "pain. She is in nursing school and returned from a medical missions trip in West Africa 10 "
            "days ago. Her symptoms began abruptly while she was shopping in a supermarket after her return. "
            "Temperature is 39.0°C (102.2°F), pulse is 100/min, respirations are 22/min, and blood pressure "
            "is 110/70 mm Hg. The patient appears ill and in mild respiratory distress. Physical examination "
            "discloses poor skin turgor and hyperactive bowel sounds. Muscle strength is 4/5 throughout. "
            "Laboratory studies show leukopenia and thrombocytopenia. Which of the following is the most "
            "sensitive and specific test for detection of the suspected viral genome in this patient?"
        ),
        "choices": {
            "A": "Microarray analysis",
            "B": "Northern blot",
            "C": "Reverse transcription-polymerase chain reaction test",
            "D": "Southern blot",
            "E": "Western blot",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 44,
        "question": (
            "A 56-year-old man comes to the office because of a 1-month history of pain and tingling of his "
            "hands and a 6-month history of paresthesia of his feet. As part of the workup, a nerve biopsy "
            "specimen is obtained and analyzed at the electron microscopic level. The biopsy specimen shows "
            "marked loss of structures labeled by the X's in the photomicrograph of a normal biopsy "
            "specimen shown. The loss of these structures is most likely to cause which of the following "
            "neurologic findings in this patient?"
        ),
        "choices": {
            "A": "Decreased sensitivity of the deep tendon reflex",
            "B": "Impaired stereognosis",
            "C": "Loss of pain and temperature sensation",
            "D": "Muscle atrophy",
            "E": "Vasoconstriction",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 45,
        "question": (
            "A 5-month-old boy is brought to the clinic by his mother because of a 10-day history of "
            "“coughing spells” that occur several times daily and last 1 to 2 minutes; he often vomits "
            "afterwards. He was delivered at term to a 16-year-old patient, gravida 1, para 1, following "
            "an uncomplicated pregnancy and spontaneous vaginal delivery in Mexico. His parents immigrated "
            "to the USA shortly after his birth. He has never been to a physician for a well-child "
            "examination and has not received any vaccinations. He appears well. Vital signs, including "
            "oxygen saturation, are within normal limits. During the physical examination, he coughs "
            "uncontrollably for 2 minutes, after which there is a gasping sound and subsequent vomiting. "
            "Afterwards, he appears exhausted. Physical examination shows no nasal flaring or intercostal "
            "or subcostal retractions. The lungs are clear; no wheezes or crackles are heard. A drug from "
            "which of the following classes is most appropriate for this patient?"
        ),
        "choices": {
            "A": "Cephalosporin",
            "B": "Fluoroquinolone",
            "C": "Macrolide",
            "D": "Penicillin",
            "E": "Sulfonamide",
        },
        "correct_answer": "C"
    },
    {
        "question_number": 46,
        "question": (
            "A 40-year-old woman comes to the physician because of a runny nose, sneezing, and itching eyes "
            "on exposure to cats since childhood. Antiallergy drugs have not provided relief. Her symptoms "
            "improve with a program of desensitization involving administration of increasing doses of the "
            "allergen. Which of the following is the most likely mechanism of the beneficial effect of "
            "this treatment?"
        ),
        "choices": {
            "A": "Formation of dimers that stimulate clearance by macrophage phagocytosis",
            "B": "Increased production of IgG antibodies that block allergen binding to mast cells",
            "C": "Overwhelming IgE binding sites to result in inactivation of mast cells",
            "D": "Production of an anti-idiotypic antibody to IgE that results in its clearance",
            "E": "Stimulation of macrophages to produce anti-inflammatory cytokines",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 47,
        "question": (
            "A 3-week-old girl delivered at term with no complications is brought to the physician by her "
            "mother because of a 1-week history of yellow eyes and skin, tan-colored stools, and dark brown "
            "urine. The newborn has been breast-feeding without difficulty. She is alert and appears to be "
            "in no distress. She is at the 50th percentile for length and weight. Physical examination shows "
            "scleral icterus and jaundice. There is mild hepatomegaly; the spleen is not palpable. "
            "Laboratory studies show:\n\nHemoglobin 14.4 g/dL\nHematocrit 43%\nLeukocyte count 8000/mm3\n\n"
            "Serum\nAlbumin 3.5 g/dL\nBilirubin, total 14 mg/dL\nDirect 12.5 mg/dL\nAST 50 U/L\nALT 45 U/L\n\n"
            "Which of the following is the most likely diagnosis?"
        ),
        "choices": {
            "A": "Biliary atresia",
            "B": "Crigler-Najjar syndrome, type I",
            "C": "Gilbert syndrome",
            "D": "Hemolytic disease of the newborn",
            "E": "Physiologic jaundice",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 48,
        "question": (
            "A 65-year-old woman comes to the physician for a follow-up examination after blood pressure "
            "measurements were 175/105 mm Hg and 185/110 mm Hg 1 and 3 weeks ago, respectively. She has "
            "well-controlled type 2 diabetes mellitus. Her blood pressure now is 175/110 mm Hg. Physical "
            "examination shows no other abnormalities. Antihypertensive therapy is started, but her blood "
            "pressure remains elevated at her next visit 3 weeks later. Laboratory studies show increased "
            "plasma renin activity; the erythrocyte sedimentation rate and serum electrolytes are within "
            "the reference ranges. Angiography shows a high-grade stenosis of the proximal right renal "
            "artery; the left renal artery appears normal. Which of the following is the most likely "
            "diagnosis?"
        ),
        "choices": {
            "A": "Atherosclerosis",
            "B": "Congenital renal artery hypoplasia",
            "C": "Fibromuscular dysplasia",
            "D": "Takayasu arteritis",
            "E": "Temporal arteritis",
        },
        "correct_answer": "A"
    },
    {
        "question_number": 49,
        "question": (
            "A 46-year-old woman comes to the physician because of a 1-month history of fatigue, weakness, "
            "and palpitations. She has advanced kidney disease as a result of continued use of combination "
            "analgesics for low back pain. She has hypertension well controlled with a loop diuretic, a "
            "β-adrenergic blocker, and a dihydropyridine calcium channel blocker. She has a history of "
            "gastritis and hemorrhoids associated with occult blood in the stools. She is in no acute "
            "distress. Her temperature is 36.8°C (98.2°F), pulse is 74/min, respirations are 14/min, and "
            "blood pressure is 150/86 mm Hg. Physical examination shows mild midepigastric tenderness to "
            "palpation and 2+ edema of the lower extremities. Cardiac examination shows an S4 gallop. Test "
            "of the stool for occult blood is positive. Laboratory studies show:\n\nHemoglobin 8.8 g/dL\n"
            "Hematocrit 26.8%\nMean corpuscular volume 82 μm3\n\nSerum\nFerritin 262 ng/mL\n"
            "Folate 284 ng/mL (N=150–450)\nTotal iron 60 μg/dL\nTransferrin saturation 22% (N=20%–50%)\n"
            "Lactate dehydrogenase 62 U/L\n\nWhich of the following is the most likely cause of this "
            "patient's anemia?"
        ),
        "choices": {
            "A": "Bone marrow suppression",
            "B": "Decreased erythropoietin production",
            "C": "Intravascular hemolysis",
            "D": "Iron deficiency anemia",
            "E": "Splenic sequestration",
        },
        "correct_answer": "B"
    },
    {
        "question_number": 50,
        "question": (
            "A 46-year-old woman comes to the physician because of a 3-day history of intermittent pain with "
            "urination and increased urinary frequency. She says that she had one similar episode during "
            "the past 6 months. She also has had irregular menses, and her last menstrual period occurred "
            "2 months ago. She has not had fever, nausea, vomiting, or blood in her urine. She is sexually "
            "active with one male partner. Physical examination shows no abnormalities. Urinalysis shows:\n\n"
            "RBC 3–5/hpf\nWBC 10–20/hpf\nNitrites positive\nLeukocyte esterase positive\nBacteria positive\n\n"
            "Which of the following is the strongest predisposing risk factor for the development of this "
            "patient's condition?"
        ),
        "choices": {
            "A": "Leiomyomata uteri",
            "B": "Perimenopause",
            "C": "Pregnancy",
            "D": "Sexual intercourse",
        },
        "correct_answer": "D"
    },
]

### ### ###
#practice_test_questions = practice_test_questions[:10] #limit to 10 to speed up testing


def call_ollama(prompt: str, model_name: str) -> str:
    """
    Sends the prompt to the Ollama API endpoint using the specified model
    and returns the text from the 'response' field in the JSON object.
    This uses a non-streaming request so we get a single JSON payload.
    Timeout is increased to 180 seconds.
    """
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "options": {
            "temperature": 0.5
        },
        "stream": False
    }

    try:
        resp = requests.post(url, json=payload, timeout=180)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama (model={model_name}): {e}")
        return ""

    response_data = resp.json()
    return response_data.get("response", "")



def call_openai(prompt: str, model_name: str) -> str:
    """
    Calls the OpenAI ChatCompletion endpoint using the given 'model_name'.
    Returns the text from the assistant's message content.
    The prompt is put into the user content of a single-turn chat. 
    Timeout of 120 seconds. 
    Make sure OPENAI_API_KEY is set in your environment 
    or set openai.api_key = 'sk-...' in your code.
    """

    client = OpenAI()
    if not client.api_key:
        client.api_key = "[YOUR_OpenAI API key_HERE" #google OpenAI API, create account on portal, create API key

    if not client.api_key:
        print("No OpenAI API key found. Cannot call OpenAI model.")
        return ""

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        print(f"Error connecting to OpenAI (model={model_name}): {e}")
        return ""

    # Extract the text from the first choice
    if not response.choices:
        return ""
    content = response.choices[0].message.content
    return content or ""

def call_model_api(prompt: str, model_info: dict) -> str:
    """
    Chooses the appropriate API caller based on model_info["engine"].
    model_info should have at least:
      {"model_name": "...", "engine": "ollama" or "openai"}
    """
    engine = model_info.get("engine", "ollama")
    model_name = model_info["model_name"]

    if engine.lower() == "openai":
        return call_openai(prompt, model_name)
    else:
        # default to ollama
        return call_ollama(prompt, model_name)

def extract_last_line(response_text: str) -> str:
    """
    Takes the entire LLM response text, splits by lines,
    and returns the last non-empty line in uppercase.
    """
    lines = [ln.strip() for ln in response_text.strip().split("\n") if ln.strip()]
    if not lines:
        return ""
    last_line = lines[-1]
    return last_line.upper()

def test_single_model(model_info: dict):
    """
    Runs the practice test on a single model, returning:
      (correct_count, total_questions, percentage_correct)
    Also prints the step-by-step results.

    model_info is a dict with:
      {
        "model_name": "xxx",
        "engine": "ollama" or "openai"
      }
    """
    model_name = model_info["model_name"]
    engine = model_info.get("engine", "ollama")

    total_questions = len(practice_test_questions)
    correct_count = 0

    for q in practice_test_questions:
        question_text = q["question"]
        choices_text = "\n".join(
            f"{letter}. {desc}" for letter, desc in q["choices"].items()
        )

        # Build prompt
        prompt = (
            "You are required to select the best answer to the question. "
            "Other options may be partially correct, but there is only ONE BEST answer. "
            "Answer the following question with exactly one letter (A, B, C, D, E, etc.) on the last line.\n\n"
            f"Question:\n{question_text}\n\n"
            f"Choices:\n{choices_text}\n\n"
            "Please provide your single-letter final answer:\n"
        )

        print(f"\n=== Model: {model_name} ({engine}) | Question {q['question_number']} ===")
        response_text = call_model_api(prompt, model_info)

        correct_answer = q["correct_answer"].upper()

        # If empty, no response -> mark incorrect
        if not response_text:
            print("No response or error from model API.")
            print(f"Model answer: None | Incorrect ❌ (Correct: {correct_answer})")
            continue

        # Extract the last line, parse a single letter
        last_line = extract_last_line(response_text)
        match = re.search(r"\b([A-E])\b", last_line, re.IGNORECASE)
        if match:
            model_answer = match.group(1).upper()
        else:
            model_answer = ""

        if model_answer == correct_answer:
            correct_count += 1
            print(f"Model answer: {model_answer} | Correct! ✅")
        else:
            print(f"Model answer: {model_answer} | Incorrect ❌ (Correct: {correct_answer})")

    percentage_correct = (correct_count / total_questions) * 100

    # Summarize for this model
    print("\n=====================================")
    print(f"Model: {model_name}  (engine={engine})")
    print(f"Result: {correct_count} / {total_questions} correct")
    print(f"Percentage correct: {percentage_correct:.1f}%")
    print("=====================================")

    return correct_count, total_questions, percentage_correct

def test_multiple_models(model_list):
    """
    Loops through each model in model_list, calls test_single_model,
    and then prints a final ranking sorted by % correct descending.

    model_list is a list of dicts, each with:
      {
        "model_name": "some_model_id",
        "engine": "ollama" or "openai"
      }
    """
    results = []  # tuples: (model_name, engine, correct_count, total, pct)

    for model_info in model_list:
        c, t, p = test_single_model(model_info)
        results.append((model_info["model_name"], model_info.get("engine","ollama"), c, t, p))

    # Sort by percentage descending
    results.sort(key=lambda x: x[4], reverse=True)

    # Print final ranking table
    print("\n\n===================== 2024 STEP-SAMPLE TEST RANKING SUMMARY =====================")
    print("{:<30} {:<8} | {:>5}  |  {}/{}".format("Model Name", "Engine", "%Corr", "Corr", "Total"))
    print("-" * 60)

    for (mname, eng, correct_count, total, pct) in results:
        print(f"{mname:<30} {eng:<8} | {pct:>5.1f}% |  {correct_count}/{total}")

    print("===========================================================")


if __name__ == "__main__":
    # Example usage: define two separate lists or a combined list of models.
    # You do not HAVE to provide openAI models. If you omit them, only the Ollama
    # ones are tested (must have Ollama installed & running, use 'ollama list' to see the model names you have installed).
    # Any model here will appear in the final ranking.

    models_to_test = [

        # OpenAI models:
        {"model_name": "gpt-4o", "engine": "openai"},
        {"model_name": "gpt-4o-mini", "engine": "openai"},
        {"model_name": "o1-mini", "engine": "openai"},
        {"model_name": "o1-preview", "engine": "openai"},

        # Ollama models:
        {"model_name": "deepseek-r1:8b-llama-distill-q8_0", "engine": "ollama"},
        #{"model_name": "deepseek-r1:7b-qwen-distill-q8_0", "engine": "ollama"}, #performed poorly
        {"model_name": "deepseek-r1:14b-qwen-distill-q4_K_M", "engine": "ollama"},
        {"model_name": "openchat:7b-v3.5-1210-q8_0", "engine": "ollama"},
        {"model_name": "llama3.1:8b-instruct-q8_0", "engine": "ollama"}

    ]

    test_multiple_models(models_to_test)
