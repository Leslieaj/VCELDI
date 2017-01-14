from parsexml import *

def indent(elem,level=0):
	i ="\n"+level* "	"
	#print elem;
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "	"
		for e in elem:
			#print e
			indent(e,level+1)
		if not e.tail or not e.tail.strip():
			e.tail =i
	if level and (not elem.tail or not elem.tail.strip()):
		elem.tail =i
	return elem

def CreateXml(template):
	model = ET.ElementTree()
	nta = ET.Element("nta")
	model._setroot(nta)
	#l = CreateDeclarationE("clock x,y;")
	#nta.append(l)
	templateE = CreateTemplateE(template)
	nta.append(templateE)
	systemE = ET.Element("system")
	systemE.text = "\n"+ "	"
	nta.append(systemE)
	queriesE = ET.Element("queries")
	queriesE.text = "\n" + "	"
	nta.append(queriesE)
	indent(nta, level=0)
	return model

def CreateDeclarationE(declaration_txt):
	#string = "// Place global declarations here."
	declaration = ET.Element("declaration")
	declaration.text = declaration_txt
	return declaration

def CreateTemplateE(template):
	templateElement = ET.Element("template")
	template_name = ET.Element("name")
	template_name.text = template.name
	templateElement.append(template_name)
	template_declaration = CreateDeclarationE(template.declaration)
	templateElement.append(template_declaration)
	for location in template.locations:
		lElement = CreateLocationE(location)
		templateElement.append(lElement)
	template_init = CreateinitE(template.initlocation)
	templateElement.append(template_init)
	for transition in template.transitions:
		tElement = CreateTransitionE(transition)
		templateElement.append(tElement)
	return templateElement

def CreateLocationE(location):
	locationElement = ET.Element("location",{"id":location.id})
	if location.name != None:
		nameElement = ET.Element("name")
		nameElement.text = location.name
		locationElement.append(nameElement)
	if location.invariant != None:
		invariantElement = ET.Element("label",{"kind":"invariant"})
		invariantElement.text = location.invariant
		locationElement.append(invariantElement)
	return locationElement

def CreateinitE(initlocation):
	if initlocation == None:
		initlocation = "id0"
	initElement = ET.Element("init",{"ref":initlocation})
	return initElement

def CreateTransitionE(transition):
	tansitionElement = ET.Element("transition")
	sourceElement = ET.Element("source",{"ref":transition.source})
	tansitionElement.append(sourceElement)
	targetElement = ET.Element("target",{"ref":transition.target})
	tansitionElement.append(targetElement)
	if transition.guard != None:
		guardElement = ET.Element("label",{"kind":"guard"})
		guardElement.text = transition.guard
		tansitionElement.append(guardElement)
	if transition.assignment != None:
		assignmentElement = ET.Element("label",{"kind":"assignment"})
		assignmentElement.text = transition.assignment
		tansitionElement.append(assignmentElement)
	return tansitionElement
	
def main():
	ntaxml = init(sys.argv[1])
	templates = parseXML(ntaxml)

	filename = "multichop.xml"
	model = CreateXml(templates[0])
	model.write(filename,"utf-8")

if __name__ == '__main__':
	main()
