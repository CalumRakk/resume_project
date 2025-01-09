
function start(){

    const data = JSON.parse(document.getElementById("__DATA__").textContent);
    const component_name= data.template_selected.componet_name;
    const component= document.createElement(component_name);
    const resumeBuilder = new ResumeBuilder(component);

}
