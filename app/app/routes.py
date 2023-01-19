from flask import render_template, url_for, flash, redirect, request
from app import app
from app.forms import PuSystemBasisForm, PuGeneratorForm, PuTransformerForm, \
        PuShortTlineForm, PuMediumTlineForm, PuLoadForm, PuForm, ClearPuObjForm, \
        GenerateAdmittanceMatrixForm, ExcelForm
from app.forms import PuSystemBasisForm, PuGeneratorForm, PuTransformerForm, \
        PuShortTlineForm, PuMediumTlineForm, PuLoadForm, PuForm, ClearPuObjForm, \
        GenerateAdmittanceMatrixForm, ExcelForm, PuSeriesImpedanceForm, \
        PuShuntImpedanceForm, PuSeriesAdmittanceForm, PuShuntAdmittanceForm, \
        PuAdmittanceForm, GoToPuConvForm, GoToAdmittanceForm, \
        GoToMatrixReductionForm, EliminateBarForm
import app.pu_convertions as pucv
import app.admitance_matrix as gam
import app.matrix_reduction as mr
import app.system_cnx_validation as scv
import app.round as round
import app.sys_components as sc
import app.pfc as pfcm



titles = ['Pu Conversion Tool', 'Register', 'Login']


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/puconversions", methods=['GET', 'POST'])
def pu_conversion():
    valid_submit = False
    valid_system_connections = True
    component_list = pucv.ValuesToComponents.get_components()
    sb_form = PuSystemBasisForm()
    gen_form = PuGeneratorForm()
    tran_form = PuTransformerForm()
    short_tline_form = PuShortTlineForm()
    medium_tline_form = PuMediumTlineForm()
    load_form = PuLoadForm()
    file_form = ExcelForm()
    pu_form = PuForm()
    
    if file_form.submit_file.data:
        if file_form.validate_on_submit():
            excel_to_objs = pucv.ExcelToValues(file_form.upload_file.data)
            excel_to_objs.create_all()
            component_list = pucv.ValuesToComponents.get_components()
            pu_form.submit_pu.data = True
    if sb_form.submit_sb.data:
        if sb_form.validate_on_submit():
            valid_submit = True
            pucv.FormToValues.sb_form_to_value(sb_form)
    if gen_form.submit_gen.data:
        if gen_form.validate_on_submit():
            valid_submit = True
            pucv.FormToValues.generator_form_to_value(gen_form)
    if tran_form.submit_tran.data:
        if tran_form.validate_on_submit():
            valid_submit = True
            pucv.FormToValues.transformer_form_to_value(tran_form)
    if short_tline_form.submit_stl.data:
        if short_tline_form.validate_on_submit():
            valid_submit = True
            pucv.FormToValues.short_tline_form_to_value(short_tline_form)
    if medium_tline_form.submit_mtl.data:
        if medium_tline_form.validate_on_submit():
            valid_submit = True
            pucv.FormToValues.medium_tline_form_to_value(medium_tline_form)
        # print(f'/routes -> medium_tline_form.validate -> component_list = {component_list}', file=sys.stderr)
    if load_form.submit_ld.data:
        if load_form.validate_on_submit():
            valid_submit = True
            pucv.FormToValues.load_form_to_value(load_form)
        # print(f'/routes -> load_form.validate -> component_list = {component_list}', file=sys.stderr)
    if pu_form.submit_pu.data:
        valid_system_connections = scv.Validation.validate_system_connections(component_list[1:])
        if valid_system_connections:
            pucv.Run(component_list).conv_to_pu()
            return redirect(url_for('pu_conversion_results'))
        else:
            flash(f"Falha de continuidade, verifique a numeração dos terminais.", 'danger')
            return redirect(url_for("pu_conversion"))

    if valid_submit:
        return redirect(url_for("pu_conversion"))
    else:
        return render_template("pu_conversions.html", title='Conversão Pu', sb_form=sb_form, pu_form=pu_form,
                                gen_form=gen_form, tran_form=tran_form, 
                                short_tline_form=short_tline_form, medium_tline_form=medium_tline_form,
                                load_form=load_form, file_form=file_form, component_list=component_list)

@app.route("/pu_conversion_results", methods=['GET', 'POST'])
def pu_conversion_results():
    clear_obj_form = ClearPuObjForm()
    generate_matrix_form = GenerateAdmittanceMatrixForm()
    component_list = pucv.ValuesToComponents.get_components()
    
    print_template = round.PrepareForTemplate()

    if clear_obj_form.submit_clear.data:
        ClearObjects.clear_all()
        return redirect(url_for('pu_conversion'))
    if generate_matrix_form.submit_matrix.data:
        gam.ConvToComponents(component_list[1:])
        return redirect(url_for('admittance_matrix_results'))
    return render_template("pu_conversion_results.html", title='Conversão Pu - Resultados', 
                            clear_obj_form=clear_obj_form, generate_matrix_form=generate_matrix_form,
                            component_list=component_list, print_template=print_template)

@app.route("/admittance_matrix", methods=['GET', 'POST'])
def admittance_matrix():
    valid_system_connections = True

    pu_zs_form = PuSeriesImpedanceForm()
    pu_zsh_form = PuShuntImpedanceForm()
    pu_as_form = PuSeriesAdmittanceForm() 
    pu_ash_form = PuShuntAdmittanceForm()
    file_form = ExcelForm()
    pu_submit_form = PuAdmittanceForm()

    form_to_components = gam.FormToComponents()
    excel_to_components = None

    # PROCESSAMENTO : 
    if file_form.submit_file.data:
        if file_form.validate_on_submit():
            excel_to_components = gam.ExcelToComponents(file_form.upload_file.data)
            pu_submit_form.submit_pu_a.data = True
    if pu_zs_form.submit_pu_zs_form.data:
        if pu_zs_form.validate_on_submit():
            form_to_components.add_component(pu_zs_form)
    if pu_zsh_form.submit_pu_zsh_form.data:
        if pu_zsh_form.validate_on_submit():
            form_to_components.add_component(pu_zsh_form)
    if pu_as_form.submit_pu_as_form.data:
        if pu_as_form.validate_on_submit():
            form_to_components.add_component(pu_as_form)
    if pu_ash_form.submit_pu_ash_form.data:
        if pu_ash_form.validate_on_submit():
            form_to_components.add_component(pu_ash_form)
    if pu_submit_form.submit_pu_a.data:
        if excel_to_components:
            component_list = excel_to_components.component_list
        else:
            component_list = form_to_components.component_list
        valid_system_connections = scv.Validation.validate_system_connections(component_list)
        if valid_system_connections:
            return redirect(url_for('admittance_matrix_results'))
            
    return render_template("admittance_matrix.html", 
                            pu_zs_form=pu_zs_form, pu_zsh_form=pu_zsh_form, pu_as_form=pu_as_form, pu_ash_form=pu_ash_form,
                            pu_submit_form=pu_submit_form, file_form=file_form,
                            title='Matrix de Admitância Nodal')

@app.route("/admittance_matrix_results", methods=['GET', 'POST'])
def admittance_matrix_results():
    go_to_pu_conv_form = GoToPuConvForm()
    go_to_admittance_form = GoToAdmittanceForm()
    go_to_reduction_form = GoToMatrixReductionForm()
    
    print_template = round.PrepareForTemplate()
    clear = ClearObjects()

    if go_to_pu_conv_form.submit_to_pu.data:
        clear.clear_all()  
        return redirect(url_for('pu_conversion'))
    if go_to_admittance_form.submit_to_matrix.data:
        clear.clear_all()  
        return redirect(url_for('admittance_matrix'))
    if go_to_reduction_form.submit_to_reduction.data:
        return redirect(url_for('matrix_reduction'))

    if 'conversion' in request.referrer:
        component_list = gam.ConvToComponents.instances[-1].component_list
    elif 'admittance_matrix' in request.referrer:
        # If am.FormToValues.instances[1].isnull True Form hasn't been used, therefore Excel has
        if gam.FormToComponents.instances[-1].isnull:
            component_list = gam.ExcelToComponents.instances[-1].component_list
        else:
            # When form has been used
            component_list = gam.FormToComponents.instances[-1].component_list
    elif 'matrix_reduction' in request.referrer: 
        kron_reduction_class = mr.KronReduction.instances[-1]
        kron_reduction_class.reduce()
        return render_template("admittance_matrix_results.html", 
                            title='Matrix de Admitância Nodal - Resultados', 
                            a_matrix_class=kron_reduction_class, print_template=print_template,
                            go_to_pu_conv_form=go_to_pu_conv_form, 
                            go_to_admittance_form=go_to_admittance_form,
                            go_to_reduction_form=go_to_reduction_form)
    a_matrix_class = gam.ComponentsToMatrix(component_list)
    return render_template("admittance_matrix_results.html", 
                        title='Matrix de Admitância Nodal - Resultados',  
                        a_matrix_class=a_matrix_class, print_template=print_template, 
                        go_to_pu_conv_form=go_to_pu_conv_form, 
                        go_to_admittance_form=go_to_admittance_form,
                        go_to_reduction_form=go_to_reduction_form)
            
@app.route("/matrix_reduction", methods=['GET', 'POST'])
def matrix_reduction():
    del_bar_form = EliminateBarForm()
    if del_bar_form.submit_bar.data:
        if del_bar_form.validate_on_submit():  
            if not mr.KronReduction.instances:
                a_matrix_class = gam.ComponentsToMatrix.instances[-1]
            else:
                a_matrix_class = mr.KronReduction.instances[-1]
            mr.KronReduction(a_matrix_class.a_matrix, del_bar_form.bar.data)
            return redirect(url_for("admittance_matrix_results"))

    return render_template("matrix_reduction.html", 
                            title='Redução Matricial',
                            del_bar_form=del_bar_form)

@app.route("/pfc", methods=['GET', 'POST'])
def pfc():
    file_form = ExcelForm()
    excel_to_components = None

    if file_form.submit_file.data:
        if file_form.validate_on_submit():
            excel_to_components = gam.ExcelToComponents(file_form.upload_file.data)
            pfcm.ExcelToObjs(file_form.upload_file.data) 
            return redirect(url_for("pfc_results"))

    return render_template("pfc.html", 
                            title='Problema do Fluxo de Carga',
                            file_form=file_form)

@app.route("/pfc_results", methods=['GET', 'POST'])
def pfc_results():
    go_to_pu_conv_form = GoToPuConvForm()
    go_to_admittance_form = GoToAdmittanceForm()
    go_to_reduction_form = GoToMatrixReductionForm()
    
    print_template = round.PrepareForTemplate()
    clear = ClearObjects()


    if go_to_pu_conv_form.submit_to_pu.data:
        clear.clear_all()  
        return redirect(url_for('pu_conversion'))
    if go_to_admittance_form.submit_to_matrix.data:
        clear.clear_all()  
        return redirect(url_for('admittance_matrix'))
    if go_to_reduction_form.submit_to_reduction.data:
        return redirect(url_for('matrix_reduction'))

    if 'pfc' in request.referrer:
        component_list = gam.ExcelToComponents.instances[-1].component_list
        a_matrix_class = gam.ComponentsToMatrix(component_list)
        tolerance = pfcm.ExcelToObjs.instances[-1].tolerance
        newton_raphson_cls = pfcm.NewtonRaphson(a_matrix_class, tolerance)
        newton_raphson_cls.solve()
        bars_df = sc.Bars.get_bars_df()
    
    a_matrix_class = gam.ComponentsToMatrix(component_list)
    return render_template("pfc_results.html", 
                        title='Problema do Fluxo de Carga - Resultados',  
                        a_matrix_class=a_matrix_class, 
                        bars_df=bars_df,
                        print_template=print_template, 
                        go_to_pu_conv_form=go_to_pu_conv_form, 
                        go_to_admittance_form=go_to_admittance_form,
                        go_to_reduction_form=go_to_reduction_form)


####################################### deleting objects ############################################
class ClearObjects():
    @classmethod
    def clear_all(cls):
        sc.Generators.del_instances()
        sc.Transformers.del_instances()
        sc.ShortTLines.del_instances()
        sc.MediumTLines.del_instances()
        sc.Loads.del_instances()
        sc.Bars.del_instances()
        sc.Components.del_instances()
        pucv.PuConvesions.del_instances()
        pucv.ValuesToComponents.del_component_list()
        pucv.Run.del_instances()
        gam.ExcelToComponents.del_instances()
        gam.FormToComponents.del_instances()
        gam.ConvToComponents.del_instances()
        gam.ComponentsToMatrix.del_instances()
        mr.KronReduction.del_instances()