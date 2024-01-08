const jsonUrl = 'directory_structure.json';



/**
 * modelObj structure:
 * {
 * 'modelA': {
 *      'experimentA': {
 *          'quantizationA': {
 *              'drugA': [
 *                  {
 *                   "filename":"A_dose_05__8bit.md",
 *                   "dose_theta":0.05,
 *                   "filepath":"./Alan_Watts/7B/Llama2/Llama-2-7b-chat-hf/8bit/A/A_dose_05__8bit.md"
 *                   },
 *                 ...
 *                 { "filename":"A_dose_80__8bit.md",
 *                   "dose_theta":0.80,
 *                   "filepath":"./Alan_Watts/7B/Llama2/Llama-2-7b-chat-hf/8bit/A/A_dose_80__8bit.md"
 *                  }
 *               ],
 *              'drugB': {...},
 *              ...,
 *              'drugN': {...},
 *          },
 *          'quantizationB': {...},
 *          ...
  *         'quantizationN': {...},
 *      },
 *      'experimentB': {...},
 *      ...,
 *      'experimentN': {...},
 *  },
 * 'modelB': {...},
 * ... 
 * 'modelN': {...},
 * }
 * 
 */

/**
 * HTML structure:
 *  model_selector (select menu)
 *  experiment_selector (select menu)
 *  quantization_selector (radiogroup)
 *  drug_type (radiogroup)
 *  diff_container
 *      left_content
 *          dose_selector (slider)
 *          seed_selector (radiogroup)
 *          text_content  (content of .md file)
 *      right_content
 *          dose_selector (slider)
 *          seed_selector (radiogroup)
 *          text_content  (content of .md file)
 *  
 * 
 */



const menu_container = document.getElementById("menuContainer")
const model_options= document.querySelector("#model_options")
const gen_info = document.querySelector(".generation_config")

var leftDoseSlider = document.getElementById('thetaslider_left');
var rightDoseSlider = document.getElementById('thetaslider_right');

const leftseedcont = document.querySelector("#left_text .text_content")
const leftseedoutercont = leftseedcont.closest(".seed_content")
leftseedcont.fieldsetelem = leftseedoutercont.querySelector("fieldset")
leftseedcont.sidestring = "left"
const rightseedcont = document.querySelector("#right_text .text_content")
const rightseedoutercont = rightseedcont.closest(".seed_content")
rightseedcont.fieldsetelem = rightseedoutercont.querySelector("fieldset")
rightseedcont.sidestring = "right"

//const leftGenConfigContainer = leftseedoutercont.parentElement.querySelector(".generation_config")
//const rightGenConfigContainer = rightseedoutercont.parentElement.querySelector(".generation_config")

const required_dose_thetas = [0.01, 0.05, 0.1, 0.15, 0.2, 0.35, 0.5, 0.8, 1]
let models = {}
let default_left = "H_dose_001__16bit.md"
let default_right = "H_dose_010__16bit.md"
// Fetch the JSON structure

function updateParents(obj, deptharr){
    Object.entries(obj).forEach(([key, value], index) => {
            if(isSpecial(key)) return;
            value.parent = obj;
            if(value.obj_name == null || value.obj_name == value.parent.obj_name || value.parent.obj_name == "experiments") 
                value.obj_name = key
            if(deptharr.length == 0) return
            if(deptharr[0] != null && typeof deptharr != "string")
                value.type = deptharr[0]
            let newdeptharr = deptharr.slice(1)
            if(newdeptharr.length > 0)
                updateParents(value, newdeptharr)
        }
    )
}

async function begin(){
    let response = await fetch(jsonUrl);
    let dir_struct = await response.json();
    dir_augment(dir_struct, '.', null, 'root')
    let models_arr = return_deep(dir_struct, 3)
    for(let i =0; i< models_arr.length; i++) {        
        let model = models_arr[i];
        let model_name = model.obj_name
        let merged_name = model.parent.parent.obj_name+"-"+model.parent.obj_name+'-'+model_name;
        if(models[merged_name] == null) {
            models[merged_name] = {obj_name : merged_name}//{'DOMelem' : model_container.cloneNode(true)}
            //model_options.appendChild(models[merged_name].DOMelem)
        }
        if(models[merged_name]['experiments'] == null) {
            models[merged_name]['experiments'] = {}
            models[merged_name]['experiments'].parent = models[merged_name]
            models[merged_name]['experiments']
        }
        
        models[merged_name]['experiments'][model.parent.parent.parent.obj_name] = model
    }
    updateParents(models, ["model", null, "experiment","quantization","drug","dose"])
    let filesArr = return_deep(models, 5)
    filemap = {}
    for(f of filesArr){
        filemap[f.filename] = f
    }
    let defaultobj = filemap[default_right]
    currentLeftDose = filemap[default_left];
    currentRightDose = defaultobj;
    maybe_load(currentLeftDose)
    maybe_load(currentRightDose)
    await currentLeftDose.ready
    await currentRightDose.ready
    currentLeftDose.parsed_md = parse_md(currentLeftDose)
    currentRightDose.parsed_md = parse_md(currentRightDose)
    currentLeftSeed = currentLeftDose.parsed_md.generations['420']
    currentRightSeed = currentRightDose.parsed_md.generations['421']
    
    let defaultchain = [currentRightSeed]
    let revChain = [{'obj_name':420, 'type': 'seed'}]
    
    while(defaultobj.parent != null) {
        defaultchain = [defaultobj, ...defaultchain]
        revChain.push(defaultobj)
        defaultobj = defaultobj.parent
    }
    
    updateModelSelector()
    for(o of defaultchain) {
        if(o.type == "model")
            currentModel = o
        if(o.type == "experiment")
            currentExperiment = o
        if(o.type == "quantization")
           currentQuantization = o
        if(o.type == "drug")
            setDrugType(o)
        if(o.type == "dose") {
            currentRightDose=o
        }
    }
    for(o of defaultchain) {
        if(o.type == "model")
            setModel(o)
        if(o.type == "experiment")
            setExperiment(o)
        if(o.type == "quantization")
            setQuantization(o)
        if(o.type == "drug")
            setDrugType(o)
        if(o.type == "dose")
            setLeftDose(o)
    }
}

function setModel(model) {
    currentModel = model.experiments;
    const modelSelector = document.getElementById('model_selector');
    modelSelector.value = currentModel.parent.obj_name;
    updateAvailableExperiments(currentModel);
    setExperiment(currentExperiment)
}
function updateModelSelector() {
    let modelSelector = cloneReplace(document.getElementById('model_selector'));
   
    Object.keys(models).forEach(modname => {
        if (isSpecial(modname)) return;
        const option = document.createElement('option');
        option.value = modname;
        option.textContent = modname;
        modelSelector.appendChild(option);
    });

    modelSelector.addEventListener('change', (event) => {
        setModel(models[event.target.value]);
    });
}


function setExperiment(experiment) {
    const validatedExperiment = validateExperiment(experiment, currentModel);
    currentExperiment = validatedExperiment;
    const experimentSelector = document.getElementById('experiment_selector');
    experimentSelector.value = currentExperiment.obj_name;
    updateAvailableQuantizations(validatedExperiment);    
    setQuantization(currentQuantization)
}

//checks if the requested experiment is available for this model, selects the next closest if not.
function validateExperiment(desiredExperiment, availableObj) {
    if (hasNonSpecial(availableObj, desiredExperiment)) { //availableObj.hasOwnProperty(desiredExperiment)) {
        return desiredExperiment;
    } else if (availableObj[desiredExperiment?.obj_name] != null) {
        return availableObj[desiredExperiment?.obj_name]
    } else {
        // return the first available experiment as the next closest
        return Object.values(availableObj)[0];
    }
}
//updates experiment select dropdown to list the experiments available for current model
function updateAvailableExperiments(modelobj) {
    let experimentSelector = cloneReplace(document.getElementById('experiment_selector'));

    Object.keys(modelobj).forEach(experiment => {
        if (isSpecial(experiment)) return;
        const option = document.createElement('option');
        option.value = experiment;
        option.textContent = experiment;
        experimentSelector.appendChild(option);
    });

    experimentSelector.addEventListener('change', (event) => {
        setExperiment(modelobj[event.target.value]);
    });
}

//updates the quantization radiogroup to list only the quantizations available for current experiment of current model
function setQuantization(quantization) {
    //if(currentQuantization == null) updateAvailableExperiments(quantization)
    const validatedQuant = validateQuant(quantization, currentExperiment);
    currentQuantization = validatedQuant;
    const quantizationRadios = document.getElementsByName('quantization');
    quantizationRadios.forEach(radio => {
        if(radio.value === currentQuantization.obj_name) { // Assuming object_name is the identifier
            radio.checked = true;
        }
    });
    updateAvailableDrugs(validatedQuant);
    setDrugType(currentDrug)
}

//checks if the requested quantization level is available for this experiment, selects the next closest if not
function validateQuant(desiredQuant, availableObj) {
    if (hasNonSpecial(availableObj, desiredQuant)) {
        return desiredQuant;
    } else if (availableObj[desiredQuant?.obj_name] != null) {
        return availableObj[desiredQuant?.obj_name]
    }
    else {
        return Object.values(availableObj)[0]; // the first available quantization as the next closest
    }
}

function updateAvailableQuantizations(experimentobj) {
    let quantizationSelector = cloneReplace(document.getElementById('quantization_selector').querySelector('fieldset'));

    Object.keys(experimentobj).forEach(quantization => {
        if (isSpecial(quantization)) return;
        const radioInput = document.createElement('input');
        radioInput.type = 'radio';
        radioInput.id = quantization;
        radioInput.name = 'quantization';
        radioInput.value = quantization;

        const label = document.createElement('label');
        label.htmlFor = quantization;
        label.textContent = quantization;

        quantizationSelector.appendChild(radioInput);
        quantizationSelector.appendChild(label);
    });
    

    quantizationSelector.addEventListener('change', (event) => {
        setQuantization(experimentobj[event.target.value]);
    });
}


function setDrugType(drug) {
    //if(currentQuantization == null) updateAvailableQuantizations(drug)
    const validatedDrug = validateDrug(drug, currentQuantization);
    currentDrug = validatedDrug;
    const drugRadios = document.getElementsByName('drug');
    drugRadios.forEach(radio => {
        if(radio.value === currentDrug.obj_name) { // Assuming object_name is the identifier
            radio.checked = true;
        }
    });
    updateAvailableDoses(validatedDrug);
    setLeftDose(currentLeftDose, true)
    setRightDose(currentRightDose, true)
}

//checks if the requested drug type is available for the current quantization level is available for this experiment, selects the next closest if not
function validateDrug(desiredDrug, availableObj) {
    if (hasNonSpecial(availableObj, desiredDrug)) {
        return desiredDrug;
    } else if (availableObj[desiredDrug?.obj_name] != null) {
        return availableObj[desiredDrug?.obj_name]
    }else {
        return Object.values(availableObj)[0]; // the first available drug as the next closest
    }
}

//updates the drug radiogroup to list only the drugs available for current quantization level of current experiment on current model
function updateAvailableDrugs(quantizationObj) {
    let drugSelector = cloneReplace(document.getElementById('drug_selector').querySelector('fieldset'));

    Object.keys(quantizationObj).forEach(drug => {
        if (isSpecial(drug)) return;
        const radioInput = document.createElement('input');
        radioInput.type = 'radio';
        radioInput.id = drug;
        radioInput.name = 'drug';
        radioInput.value = drug;

        const label = document.createElement('label');
        label.htmlFor = drug;
        label.textContent = drug;

        drugSelector.appendChild(radioInput);
        drugSelector.appendChild(label);
    });

    const validatedDrug = validateDrug(currentDrug, currentQuantization);
    currentDrug = validatedDrug;

    drugSelector.addEventListener('change', (event) => {
        setDrugType(quantizationObj[event.target.value], true);
    });
}


//checks if the requested dose is available on the currently selected quantization level, selects the next closest if not
function validateDose(desiredDoseTheta, availableObjList) {
    return availableObjList[closest(desiredDoseTheta.dose_theta, availableObjList, (k, v)=>v.dose_theta)[0]]
}

async function setLeftDose(doseObj, updateSlider=false) {
    const validatedDoseObj = validateDose(doseObj, currentDrug);
    currentLeftDose = validatedDoseObj;
    // Update the UI element for left dose slider here
    
    leftDoseSlider.parentElement.parentElement.querySelector("output").value = validatedDoseObj.dose_theta
    if(validatedDoseObj.is_loaded != true) {
        leftseedoutercont.classList.add("loading_hint")
        maybe_load(validatedDoseObj)
        let loaded = await validatedDoseObj.ready
        if(loaded != undefined) {
            validatedDoseObj.parsed_md = parse_md(validatedDoseObj)
        }
        leftseedoutercont.classList.remove("loading_hint")
    }
    if(updateSlider) 
        leftDoseSlider.value = parseInt(validatedDoseObj.dose_theta*100);    
    //leftGenConfigContainer.innerHTML = validatedDoseObj.info_card
    updateAvailableLeftSeeds(validatedDoseObj.parsed_md.generations)
    setLeftSeed(currentLeftSeed, validatedDoseObj.parsed_md.generations)
    
}
async function setRightDose(doseObj, updateSlider = false) {
    const validatedDoseObj = validateDose(doseObj, currentDrug);
    currentRightDose = validatedDoseObj;
    // Update the UI element for right dose slider here   
    rightDoseSlider.parentElement.parentElement.querySelector("output").value = validatedDoseObj.dose_theta;
    if(validatedDoseObj.is_loaded != true) {
        rightseedoutercont.classList.add("loading_hint")
        maybe_load(validatedDoseObj)
        let loaded = await validatedDoseObj.ready
        if(loaded != undefined) {
            validatedDoseObj.parsed_md = parse_md(validatedDoseObj)
        }
        rightseedoutercont.classList.remove("loading_hint")
    }

    if(updateSlider)
        rightDoseSlider.value = parseInt(validatedDoseObj.dose_theta*100);
    
    //rightGenConfigContainer.innerHTML = validatedDoseObj.info_card;
    updateAvailableRightSeeds(validatedDoseObj.parsed_md.generations)
    setRightSeed(currentRightSeed, validatedDoseObj.parsed_md.generations)
}

//updates the two dose sliders (left_dose and right_dose) to list only the doses available for current drug at current quantization level of current experiment on current model
function updateAvailableDoses(drugObj) {
    leftDoseSlider = cloneReplace(document.getElementById('thetaslider_left'));
    rightDoseSlider = cloneReplace(document.getElementById('thetaslider_right'));

    const doses = drugObj.map(dose => dose.dose_theta);
    const minDose = Math.min(...doses);
    const maxDose = Math.max(...doses);

    [leftDoseSlider, rightDoseSlider].forEach(slider => {
        slider.min = minDose*100;
        slider.max = maxDose*100;
        slider.step = 1;
        //slider.setAttribute("step", "any")//(maxDose - minDose) / doses.length;
    });    

    leftDoseSlider.addEventListener('input', (event) => {
        setLeftDose(drugObj[closest(parseFloat(event.target.value)/100, drugObj, (k, v)=>v.dose_theta)[0]]);
    });
    leftDoseSlider.addEventListener('change', (event) => {
        setLeftDose(drugObj[closest(parseFloat(event.target.value)/100, drugObj, (k, v)=>v.dose_theta)[0]], true);
    });

    rightDoseSlider.addEventListener('input', (event) => {
        setRightDose(drugObj[closest(parseFloat(event.target.value)/100, drugObj, (k, v)=>v.dose_theta)[0]]);
    });
    rightDoseSlider.addEventListener('change', (event) => {
        setRightDose(drugObj[closest(parseFloat(event.target.value)/100, drugObj, (k, v)=>v.dose_theta)[0]], true);
    });
}


function validateSeed(desiredSeed, availableSeeds){
    if(availableSeeds[desiredSeed.obj_name] == desiredSeed)
        return desiredSeed
    else {
        let closestSeed = closest(parseInt(desiredSeed.obj_name), availableSeeds, (i, v, k) => v.obj_name)
        return availableSeeds[closestSeed[1]]
    }
}


async function setLeftSeed(seedObj, availableSeeds) {
    const validatedSeedObj = validateSeed(seedObj, availableSeeds);
    prevLeftSeed = currentLeftSeed
    currentLeftSeed = validatedSeedObj == null ? currentLeftSeed : validatedSeedObj
    updateSeedDisplay(seedObj, leftseedcont)
}
async function setRightSeed(seedObj, availableSeeds) {
    const validatedSeedObj = validateSeed(seedObj, availableSeeds);
    prevRightSeed = currentRightSeed
    currentRightSeed = validatedSeedObj;// == null ? currentRightSeed : validatedSeedObj
    updateSeedDisplay(seedObj, rightseedcont)
}


function updateAvailableSeeds(seedObj, side) {
    let seedSelector = cloneReplace(side.fieldsetelem);
    side.fieldsetelem = seedSelector;
    let seedsidestring = side.sidestring
    Object.keys(seedObj).forEach(seed => {
        if (isSpecial(seed)) return;
        const radioInput = document.createElement('input');
        radioInput.type = 'radio';
        radioInput.id =  seedsidestring+'_'+seed;
        radioInput.name = seedsidestring+'_seed';
        radioInput.value = seed;

        const label = document.createElement('label');
        label.htmlFor =  seedsidestring+'_'+seed;
        label.textContent = seed;

        seedSelector.appendChild(radioInput);
        seedSelector.appendChild(label);
    });
    

    seedSelector.addEventListener('change', async (event) => {
        if(side == leftseedcont ) {
            if(currentLeftDose.is_loading || currentLeftDose.is_loaded != true) {
                let ready= await currentLeftDose.ready;
            }
            setLeftSeed(seedObj[event.target.value], currentLeftDose.parsed_md.generations);
        }
        if(side == rightseedcont) {
            if(currentRightDose.is_loading || currentRightDose.is_loaded != true) {
                let ready= await currentRightDose.ready;
            }
            setRightSeed(seedObj[event.target.value], currentRightDose.parsed_md.generations);
        }
    });
}

function updateAvailableLeftSeeds(generationsObj) {
    updateAvailableSeeds(generationsObj, leftseedcont);
}

function updateAvailableRightSeeds(generationsObj) {
    updateAvailableSeeds(generationsObj, rightseedcont);
}

async function updateSeedDisplay(seedObj, side) {
    let text_container = side
    text_container.textObj = seedObj.text_content
    let thistext = seedObj.text_content
    if(currentLeftDose.is_loaded != true) await currentLeftDose.ready
    if(currentRightDose.is_loaded != true) await currentRightDose.ready
    let otherObj = side == rightseedcont ? currentLeftSeed : currentRightSeed
    let othertext = otherObj?.text_content 
    let seedsidestring = side.sidestring
    let othertext_container = side == rightseedcont ? leftseedcont : rightseedcont
    if(othertext != undefined) {        
        console.log("other seed: " + otherObj.obj_name)
        text_container.textContent = thistext
        //othertext_container.textContent = othertext
        let othernew = createDiff(othertext, thistext)
        let thisnew = createDiff(thistext, othertext)
        text_container.innerHTML = thisnew
        othertext_container.innerHTML = othernew
        updateCard(currentLeftDose, currentRightDose)
    } else {
        text_container.textContent = thistext
    }
    const seedRadios = document.getElementsByName(seedsidestring+'_seed');
    seedRadios.forEach(radio => {
        if(radio.value === seedObj.obj_name) {
            radio.checked = true;
        }
    });
}

function getSeedSideString(side) {
    let result ="left";
    if(side.closest("#right_text") != null) result = "right"
    return result
}


function parse_md(doseobj) {
    let text = doseobj.md_text;

    // Define patterns for different sections
    const systemPattern = /## System:\s*###\s*"([^"]+)"/;
    const promptPattern = /## Prompt:\s*"([^"]+)"/;
    const postSamplingPattern = /## post-sampling method:\s*###\s*([^\n]+)/;
    const configPattern = /### Config\s*([\s\S]*?)```/;
    const responsePattern = /Seed: (\d+)\s*```([\s\S]*?)```/g;

    // Extract data using patterns
    const system = systemPattern.exec(text)[1];
    const prompt = promptPattern.exec(text)[1];
    const postSampling = postSamplingPattern.exec(text)[1];
    const config = configPattern.exec(text)[1].trim();

    // Extract and build generations
    let match;
    let generations = {};
    while ((match = responsePattern.exec(text)) !== null) {
        generations[match[1]] = {
            'text_content': match[2].trim(),
            'type': 'seed',
            'parent': generations,
            'obj_name': match[1]};
    }
    generations.parent = doseobj;

    // Build and return the final structured object
    return {
        system: system,
        prompt: prompt,
        post_sampling: postSampling,
        config: config,
        generations: generations,
        parent: doseobj,
        type: "config"
    };
}

async function maybe_load(obj, oncomplete){
    //console.log("load requested!")
    if(obj.is_loaded != true && obj.is_loading != true) {
        console.log("is_loaded="+obj.is_loaded +", is_loading="+obj.is_loading+", obj_name= " +JSON.stringify(obj.filename))
        obj.is_loading = true
        obj.is_loaded = false
        let res, rej;
        obj.ready = new Promise((y, n) => {res = y; rej = n;})
        if(obj.filepath.substring(0, 2) == ".//") 
            obj.filepath = obj.filepath.substring(2)
        let fetchwait = await fetch(obj.filepath)
        obj.md_text = await fetchwait.text()
        obj.info_card = marked.parse(obj.md_text.split("# RESPONSES")[0]);
        res("done")
        obj.is_loaded = true;
        obj.is_loading = false;
        if(oncomplete != undefined)
            oncomplete(obj);
    } else if (obj.is_loading) {
        //console.log("STILLLOADING STILLLOADING STILLLOADING")
        let res = await obj.ready
        obj.is_loaded = true;
        if(oncomplete != undefined)
            return oncomplete(null)
    } else {
        //console.log("already did")
        if(oncomplete != undefined)
            oncomplete(null)        
    }
}
async function updateCard(leftDoseObj, rightDoseObj) {
    let DomCard = document.querySelector(".generation_config")
    if(leftDoseObj.is_loaded != true || leftDoseObj.is_loading == true) {
        await leftDoseObj.ready
    }
    let left_card_html = leftDoseObj.info_card
    if(rightDoseObj.is_loaded != true || rightDoseObj.is_loading == true) {
        await rightDoseObj.ready
    }
    let right_card_html = rightDoseObj.info_card
    DomCard.innerHTML = left_card_html
    let leftCode = getLastCodeElem(left_card_html)
    let rightCode = getLastCodeElem(right_card_html)
    augmentThetaString(DomCard, leftDoseObj.dose_theta, rightDoseObj.dose_theta)
    wrapLastCode(DomCard, leftCode, rightCode)
    
}
function getLastCodeElem(virtual_info_card) {
    let aselem = document.createElement("div")
    aselem.innerHTML = virtual_info_card
    let allcodes = aselem.querySelectorAll("pre")
    let lastcode = allcodes[allcodes.length-1]
    return lastcode
}
function wrapLastCode(DOM_info_card, newleft, newright) {
    let codeWrapper = DOM_info_card.querySelector(".diffcode")
    if(codeWrapper == null) {
        let allcodes = DOM_info_card.querySelectorAll("pre")
        let lastcode = allcodes[allcodes.length-1]
        let codesib = lastcode.nextElementSibling
        let codepar = lastcode.parentElement
        lastcode.remove();
        codeWrapper = document.createElement("div")
        codeWrapper.classList.add("diffcode")
        codepar.insertBefore(codeWrapper, codesib)
    } else {
        codeWrapper.innerHTML('')
    }   
    codeWrapper.appendChild(newleft)
    codeWrapper.appendChild(newright)
}

function augmentThetaString(DOM_info_card, lefttheta, righttheta) {
    let thetaelem = DOM_info_card.querySelector("p")
    thetaelem.innerHTML = "<div class='split_thetas'><div class='left_info_theta'>dose_theta = "+lefttheta+"</div>"+"<div class='right_info_theta'>dose_theta = "+righttheta+"</div></div>"
}

function createDiff(thistext, othertext) {
    let dmp = new diff_match_patch();
    dmp.Diff_EditCost = 5; 
    let text1 = othertext;
    let text2 = thistext;
  
    let d = dmp.diff_main(text1, text2);
    dmp.diff_cleanupSemantic(d);
    let tempnode = document.createElement("span");
    let tmphtml = dmp.diff_prettyHtml(d).replace(/&para;/g, '');
    tempnode.innerHTML = tmphtml;
    let delnodes = tempnode.querySelectorAll("del")
    delnodes.forEach(del => {
        del.innerHTML = '<span class="hoverdel">'+del.innerHTML+'</span>';
    })
    return tempnode.innerHTML
  }

function dir_augment(j, current_dir, parent, obj_name) {
    
    if(Array.isArray(j)) {
        for(let i =0; i<j.length; i++) {
            dir_augment(j[i], current_dir, j, null)
        }
    } else {
        j['parent'] = parent
        j['obj_name'] = obj_name
        if(j["filename"] != undefined) {
            j["directory"] = current_dir;
            if(current_dir.substring(0,1) != '/')
                j["filepath"] = current_dir+"/"+j["filename"];
            return
        } else {
            Object.keys(j).forEach(k=> {
                if(k == '__py_cache__') {
                    delete j[k]
                    return;
                } else {
                    if(k!='parent' && k != 'obj_name')
                        dir_augment(j[k], current_dir+"/"+k, j, k)
                }
            })
        }
    }
}

function return_deep(from, recurse) {
    //console.log(from.obj_name)
    let result = []
    if(recurse == 0) {
        Object.keys(from).forEach(k=>{
            if(!isSpecial(k)) {
                result.push(from[k])
            }
        })
    } else {
        
        if (Array.isArray(from)) {
            for(let i=0; i<from.length; i++) {
                result = result.push(...return_deep(from[i], recurse-1))
            }
        } else {
            Object.keys(from).forEach(k=>{
                if(!isSpecial(k)) {
                    let v = from[k]
                    if (v!= null)
                        result.push(...return_deep(v, recurse-1))
                        //console.log(result)
                }
            })
        }
    }
    return result
}


function closest(target, maybearray, checkby) {
    if(checkby == null) {
        checkby = (key, val) => {return val}
    }
    let closestNum = null
    let closest_idx = 0
    let closest_k = null
    let closest_val = null
    let minDiff = Math.abs(target - closestNum);
    Object.entries(maybearray).forEach(([k, v], i) => {
        const diff = Math.abs(target - checkby(i, v, k));
        if (diff < minDiff || closestNum == null) {
            minDiff = diff;
            closestNum = checkby(i, v, k);
            closest_k = k
            closest_val = v
            closest_idx = i
        }
    })
    return [closest_idx, closestNum, closest_val, closest_k];
}

function isSpecial(key) {
    if(key == 'parent' || key =='DOMelem' || key == 'obj_name' || key=='type')
        return true
}
function hasNonSpecial(haystack, needle) {
    let result = false;
    Object.keys(haystack).forEach(k=>{
        if(isSpecial(k)) return
        if(haystack[k] == needle) result = needle;
    })
    return result
}

function cloneReplace(elem){
    let reinsert = null
    if (elem.tagName == "FIELDSET") {
        reinsert = elem.querySelector("legend")
    }
    let origPar = elem.parentElement
    let sib = elem.nextElementSibling
    let clone = elem.cloneNode(false)
    elem.remove()
    origPar.insertBefore(clone, sib)
    if(reinsert != null)
        clone.appendChild(reinsert)
    return clone
}


begin()