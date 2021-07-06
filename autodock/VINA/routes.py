import pandas as pd
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from vina import Vina
import os
from autodock import helpers

mainapp = Blueprint("mainapp", __name__, template_folder='./templates')


def process_protein_ligand(protein, ligand, config, n, rand_seed):
    v = Vina()
    protein.save(f"./autodock/input/protein_{rand_seed}.pdbqt")
    ligand.save(f"./autodock/input/ligand_{rand_seed}.pdbqt")
    v.set_receptor(f"./autodock/input/protein_{rand_seed}.pdbqt")
    v.set_ligand_from_file(f"./autodock/input/ligand_{rand_seed}.pdbqt")
    print(type(config.center_x))
    v.compute_vina_maps(center=[config.center_x, config.center_y, config.center_z],
                        box_size=[config.size_x, config.size_y, config.size_z])
    v.score()
    v.optimize()
    v.write_pose(f'./autodock/output/protein_ligand_{rand_seed}_{n}.pdbqt', overwrite=True)
    return f'protein_ligand_{rand_seed}_{n}.pdbqt'


async def multiprocess_files(p_list, l_list, conf, rnd):
    conf = conf.astype(float)
    outfiles = []
    for i in range(len(conf)):
        outfiles.append(process_protein_ligand(p_list[i], l_list[i], conf.iloc[i, :], i+1,  rnd[i]))
    return outfiles


@mainapp.route('/output/<path:path>')
def output(path):
    return send_from_directory('output', path)


@mainapp.route('/', methods=["GET", "POST"])
async def home():
    down = False
    out = None
    if request.method == "POST":
        pf = request.files.getlist("proteinFiles")
        lf = request.files.getlist("ligandFiles")
        conf = pd.read_csv(request.files["paramFile"])
        rnd = list(request.form["randomval"].split(','))
        out = await multiprocess_files(pf, lf, conf, rnd)
        down = True
    return render_template('home.html', down=down, out=out)


@mainapp.post("/getnrows")
def n_api():
    file = request.files["csvfile"]
    file = pd.read_csv(file)
    return jsonify({"nrows": len(file)})
