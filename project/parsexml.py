# decode the uppaal xml
# only location, transition
# transiton : only guard and assignment

import sys
import xml.etree.cElementTree as ET

class NTA:
    def __init__(self, declaration="", system="", templates=None):
        self.declaration = declaration
        self.system = system
        self.templates = templates or []

class Template:
	def __init__(self, name, declaration="", locations=None, initlocation=None, transitions=None):
		self.name = name
		self.declaration = declaration
		self.locations = locations or []
		self.initlocation = initlocation
		self.transitions = transitions or []

class Label:
	def __init__(self, kind, value=None):
		self.kind = kind
		self.value = value

class Location:
	def __init__(self, id, name=None, invariant=None, init=False, transitions=[]):
		self.id = id
		self.name = name
		self.invariant = invariant
		self.init = init
		self.next = self.initNexttransition(transitions) or {}
	def initNexttransition(self, transitions):
		nexttr = {}
		for tr in transitions:
			if tr.source == self.id:
				nexttr[tr.id] = False
		return nexttr
	def getlocation(self):
		return [self.id, self.name, self.invariant, self.init, self.next]


class Transition:
	def __init__(self, id, source, target, guard=None, assignment=None):
		self.id = id
		self.source = source
		self.target = target
		#self.guard = Label("guard", guard)
		#self.assignment = Label("assignment", assignment)
		self.guard = guard
		self.assignment = assignment
	def gettransition(self):
		return [self.id, self.source, self.target, self.guard, self.assignment]
		
"""class Nexttransitions:
	def __init__(self, locationid, template):
		self.location = locationid
		self.next = self.initNexttransition(template) or {}

	def initNexttransition(self, template):
		nexttr = {}
		for tr in template.transitions:
			if tr.source == self.location:
				nexttr[tr.id] = False
		return nexttr"""

def init(xmlfile):
	tree = ET.parse(xmlfile)
	root = tree.getroot()
	return root

def parseXML(root):
	declaration = root.findtext('declaration') or ""
	system = root.findtext('system') or ""
	templates = []
	transitionid = 1
	for templatexml in root.getiterator("template"):
		declaration = templatexml.findtext("declaration") or ""
		transitions = []
		for transitionxml in templatexml.getiterator("transition"):
			sourceL = transitionxml.find('source').get('ref')
			targetL = transitionxml.find('target').get('ref')
			transition = Transition(transitionid,sourceL,targetL,)
			transitionid = transitionid + 1
			for labelxml in transitionxml.getiterator("label"):
				"""if labelxml.get('kind') in ['guard','assignment']
					label = getattr(transition, labelxml.get('kind'))
					label.value = labelxml.text"""
				if labelxml.get('kind') == 'guard':
					transition.guard = labelxml.text
				if labelxml.get('kind') == 'assignment':
					transition.assignment = labelxml.text
			transitions += [transition]
		locations = []
		for locationxml in templatexml.getiterator("location"):
			name = locationxml.findtext("name")
			location = Location(id=locationxml.get('id'),name=name, transitions=transitions)
			for labelxml in locationxml.getiterator("label"):
				if labelxml.get('kind') == 'invariant':
					location.invariant = labelxml.text
			locations += [location]
		if templatexml.find("init") != None:
			initlocation = templatexml.find("init").get('ref')
			for l in locations:
				if l.id == templatexml.find("init").get('ref'):
					l.init = True
		else:
			initlocation = None
		template = Template(templatexml.find("name").text,declaration,locations=locations,initlocation=initlocation,transitions=transitions)
		templates += [template]
	return templates

def main():
	ntaxml = init(sys.argv[1])
	templates = parseXML(ntaxml)
	#next = []
	for t in iter(templates):
		print t.name, t.declaration
		for l in t.locations:
			#next+=[Nexttransitions(l.id, t)]
			print l.getlocation()
		for tr in t.transitions:
			print tr.gettransition()

	#for i in next:
		#print i.location, i.next

if __name__=='__main__':
	main()

