
import torch

from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#salloc --time=1:0:0 --gres=gpu:v100l:1 --cpus-per-task=16 --mem=63500M --ntasks=1 --account=def-pimentel
#python run.py
#python stable-diffusion/scripts/txt2img.py --prompt "a photograph of an astronaut riding a horse" --plms 
xm = load_model('transmitter', device=device)
model = load_model('text300M', device=device)
diffusion = diffusion_from_config(load_config('diffusion'))

batch_size = 10
guidance_scale = 20.0
prompt = ["a person that looks like Jesus Christ doing a t pose"]

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

    # Example of saving the latents as meshes.
    from shap_e.util.notebooks import decode_latent_mesh

    for j, latent in enumerate(latents):
        t = decode_latent_mesh(xm, latent).tri_mesh()
        with open(f'{prompt[i]}{j}.obj', 'w') as f:
            t.write_obj(f)