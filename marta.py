import spacy
import os
import torch
from nlp.generic_scene_dictionary import generic_settings
from nlp.generic_dictionary import generic
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import decode_latent_mesh
from rigging.master_rigger import rig
from rendering.render_runner import render
from nlp.filter import classify_verb, detect_setting, water

#Initiates spacy nlp model and processes user input 
nlp = spacy.load("en_core_web_sm")
para="A man walking on the beach"
doc = nlp(para)

pnoun=[]            #Proper Nouns
anouns=[]           #Nouns
prompt=[]           #Prompts, contains edited text, e.g 'tpose', 'a person'
saved=[]            #Original names of the prompts, using it as savefile name of prompts as its unedited
setting=[]          #Story setting
action=[]           #Verbs
requiredanim=[]     #Required animations
location = detect_setting(para) #Detect setting
animations = os.listdir("animations") #Get animation library

#Adding values to arrays
for token in doc:
    if spacy.explain(token.pos_) == "noun":
        for key in generic:
            if key == (str(token).lower()):
                prompt.append(generic[str(token)] + " in a t pose")
        anouns.append(str(token))
        saved.append(str(token))
    elif spacy.explain(token.pos_) == "proper noun":
        pnoun.append(str(token))
        saved.append(str(token))      
    elif spacy.explain(token.pos_) == "verb":
        action.append(str(token))

#Create prompts for location/setting
for i in location:
    for key in generic_settings:
        if i == key:
             setting.append(generic_settings[i])
             
#Find and append necessary verbs according to the prompt
classified_verbs = [classify_verb(verb) for verb in action]
for i in classified_verbs:
    print(i)
    for j in animations:
        if f'{i}.fbx'.lower()==j.lower():
            requiredanim.append(j)
               
#Generate 2D assets
for i in range(0,len(setting)):
    os.system(f"python scripts/txt2img.py --prompt \'{str(setting[i])}\'  --skip_grid --plms")
for i in location:
   for key in generic_settings:
       if i == key:
           os.system(f"python scripts/txt2img.py --prompt \'{str(i)} ground texture\'  --skip_grid --plms") 

#Shap-E 3d model loader
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))

#Generate 3d assets
batch_size = 1
guidance_scale = 20.0
for i in range(0,len(prompt)):
 
    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt[i]] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=64,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )

    render_mode = 'nerf' # you can change this tso 'stf'
    size = 512 # this is the size of the renders; higher values take longer to render.

    for j, latent in enumerate(latents):
        t = decode_latent_mesh(xm, latent).tri_mesh()
        with open(f'3doutputs/{saved[i]}.obj', 'w') as f:
            t.write_obj(f)

#Load file names for rigging process     
outputs2d = os.listdir("2doutputs")
outputs3d = os.listdir("3doutputs")
watertrue=water(prompt)

#Rig 3d model with animation file
rig(f"3doutputs/{outputs3d[0]}",f"animations/{requiredanim[0]}",f"rigged/{anouns[0]}{requiredanim[0]}",2)

#Generate scene file
rigged = os.listdir("rigged")
f=open("main.scene","w+")
f.write(f"BACKGROUND_IMAGE 2doutputs/{outputs2d[0]}\n")
if watertrue:
    f.write("USE_WATER True\n")
f.write(f"GROUND_IMAGE 2doutputs/{outputs2d[1]}\n")
f.write("USE_CYCLES False\n")
f.write("CHARACTER_SCALE 2\n")
f.write("\n")
f.write(f"CHARACTER {anouns[0]}\n")
f.write(f"anim {requiredanim[0]} rigged/{rigged[0]}\n ")
f.write("\n")
f.write("ANIMATION\n")
f.write(f"{anouns[0]} position 0 -2 0 0\n")
if requiredanim[0] == "Walk.fbx" or requiredanim[0] =="Run.fbx":
    f.write(f"{anouns[0]} path {requiredanim[0]} -6 -2 0 6 -2 0 0\n")
else:
    f.write(f"{anouns[0]} loop_anim {requiredanim[0]} 0 100\n")
f.close()

#Render animation using scene file
render("main.scene","videooutput/animation.mp4")

