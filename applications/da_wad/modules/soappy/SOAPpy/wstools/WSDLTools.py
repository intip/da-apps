# Copyright (c) 2001 Zope Corporation and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.

ident = "$Id: WSDLTools.py,v 1.14 2003/12/23 07:56:31 warnes Exp $"

from Utility import DOM, Collection
from XMLSchema import XMLSchema, SchemaReader, WSDLToolsAdapter
from StringIO import StringIO
import urllib

class WSDLReader:
    """A WSDLReader creates WSDL instances from urls and xml data."""

    # Custom subclasses of WSDLReader may wish to implement a caching
    # strategy or other optimizations. Because application needs vary 
    # so widely, we don't try to provide any caching by default.

    def loadFromStream(self, stream, name=None):
        """Return a WSDL instance loaded from a stream object."""
        document = DOM.loadDocument(stream)
        wsdl = WSDL()
        if name:
            wsdl.location = name
        elif hasattr(stream, 'name'):
            wsdl.location = stream.name
        wsdl.load(document)
        return wsdl

    def loadFromURL(self, url):
        """Return a WSDL instance loaded from the given url."""
        document = DOM.loadFromURL(url)
        wsdl = WSDL()
        wsdl.location = url
        wsdl.load(document)
        return wsdl

    def loadFromString(self, data):
        """Return a WSDL instance loaded from an xml string."""
        return self.loadFromStream(StringIO(data))

    def loadFromFile(self, filename):
        """Return a WSDL instance loaded from the given file."""
        file = open(filename, 'rb')
        try:
            wsdl = self.loadFromStream(file)
        finally:
            file.close()
        return wsdl

class WSDL:
    """A WSDL object models a WSDL service description. WSDL objects
       may be created manually or loaded from an xml representation
       using a WSDLReader instance."""

    def __init__(self, targetNamespace=None, strict=1):
        self.targetNamespace = targetNamespace or 'urn:this-document.wsdl'
        self.documentation = ''
        self.location = None
        self.document = None
        self.name = None
        self.services = Collection(self)
        self.messages = Collection(self)
        self.portTypes = Collection(self)
        self.bindings = Collection(self)
        self.imports = Collection(self)
        self.types = Types(self)
        self.extensions = []
        self.strict = strict

    def __del__(self):
        if self.document is not None:
            self.document.unlink()
            self.document = None

    version = '1.1'

    def addService(self, name, documentation=''):
        if self.services.has_key(name):
            raise WSDLError(
                'Duplicate service element: %s' % name
                )
        item = Service(name, documentation)
        self.services[name] = item
        return item

    def addMessage(self, name, documentation=''):
        if self.messages.has_key(name):
            raise WSDLError(
                'Duplicate message element: %s.' % name
                )
        item = Message(name, documentation)
        self.messages[name] = item
        return item

    def addPortType(self, name, documentation=''):
        if self.portTypes.has_key(name):
            raise WSDLError(
                'Duplicate portType element: name'
                )
        item = PortType(name, documentation)
        self.portTypes[name] = item
        return item

    def addBinding(self, name, type, documentation=''):
        if self.bindings.has_key(name):
            raise WSDLError(
                'Duplicate binding element: %s' % name
                )
        item = Binding(name, type, documentation)
        self.bindings[name] = item
        return item

    def addImport(self, namespace, location):
        item = ImportElement(namespace, location)
        self.imports[namespace] = item
        return item

    def load(self, document):
        # We save a reference to the DOM document to ensure that elements
        # saved as "extensions" will continue to have a meaningful context
        # for things like namespace references. The lifetime of the DOM
        # document is bound to the lifetime of the WSDL instance.
        self.document = document

        definitions = DOM.getElement(document, 'definitions', None, None)
        if definitions is None:
            raise WSDLError(
                'Missing <definitions> element.'
                )
        self.version = DOM.WSDLUriToVersion(definitions.namespaceURI)
        NS_WSDL = DOM.GetWSDLUri(self.version)

        self.targetNamespace = DOM.getAttr(definitions, 'targetNamespace',
                                           None, None)
        self.name = DOM.getAttr(definitions, 'name', None, None)
        self.documentation = GetDocumentation(definitions)

        # Resolve (recursively) any import elements in the document.
        imported = {}
        while 1:
            imports = []
            for element in DOM.getElements(definitions, 'import', NS_WSDL):
                location = DOM.getAttr(element, 'location')
                if not imported.has_key(location):
                    imports.append(element)
            if not imports:
                break
            for element in imports:
                self._import(document, element)
                location = DOM.getAttr(element, 'location')
                imported[location] = 1

        reader = SchemaReader(base_url=self.location)
        for element in DOM.getElements(definitions, None, None):
            localName = element.localName

            if not DOM.nsUriMatch(element.namespaceURI, NS_WSDL):
                if localName == 'schema':
                    schema = reader.loadFromNode(WSDLToolsAdapter(self), element)
                    schema.setBaseUrl(self.location)
                    self.types.addSchema(schema)
                else:
                    self.extensions.append(element)
                continue

            elif localName == 'message':
                name = DOM.getAttr(element, 'name')
                docs = GetDocumentation(element)
                message = self.addMessage(name, docs)
                parts = DOM.getElements(element, 'part', NS_WSDL)
                message.load(parts)
                continue

            elif localName == 'portType':
                name = DOM.getAttr(element, 'name')
                docs = GetDocumentation(element)
                ptype = self.addPortType(name, docs)
                operations = DOM.getElements(element, 'operation', NS_WSDL)
                ptype.load(operations)
                continue

            elif localName == 'binding':
                name = DOM.getAttr(element, 'name')
                type = DOM.getAttr(element, 'type', default=None)
                if type is None:
                    raise WSDLError(
                        'Missing type attribute for binding %s.' % name
                        )
                type = type.split(':', 1)[-1]
                docs = GetDocumentation(element)
                binding = self.addBinding(name, type, docs)
                operations = DOM.getElements(element, 'operation', NS_WSDL)
                binding.load(operations)
                binding.load_ex(GetExtensions(element))
                continue

            elif localName == 'service':
                name = DOM.getAttr(element, 'name')
                docs = GetDocumentation(element)
                service = self.addService(name, docs)
                ports = DOM.getElements(element, 'port', NS_WSDL)
                service.load(ports)
                service.load_ex(GetExtensions(element))
                continue

            elif localName == 'types':
                self.types.documentation = GetDocumentation(element)
                for item in DOM.getElements(element, None, None):
                    if item.localName == 'schema':
                        schema = reader.loadFromNode(WSDLToolsAdapter(self), item)
                        schema.setBaseUrl(self.location)
                        self.types.addSchema(schema)
                    else:
                        self.types.addExtension(item)
                continue

    def _import(self, document, element):
        namespace = DOM.getAttr(element, 'namespace', default=None)
        location = DOM.getAttr(element, 'location', default=None)
        if namespace is None or location is None:
            raise WSDLError(
                'Invalid import element (missing namespace or location).'
                )

        # Sort-of support relative locations to simplify unit testing. The
        # WSDL specification actually doesn't allow relative URLs, so its
        # ok that this only works with urls relative to the initial document.
        location = urllib.basejoin(self.location, location)

        obimport = self.addImport(namespace, location)
        obimport._loaded = 1

        importdoc = DOM.loadFromURL(location)
        try:
            if location.find('#') > -1:
                idref = location.split('#')[-1]
                imported = DOM.getElementById(importdoc, idref)
            else:
                imported = importdoc.documentElement
            if imported is None:
                raise WSDLError(
                    'Import target element not found for: %s' % location
                    )

            imported_tns = DOM.findTargetNS(imported)
            if imported_tns != namespace:
                return

            if imported.localName == 'definitions':
                imported_nodes = imported.childNodes
            else:
                imported_nodes = [imported]
            parent = element.parentNode
            for node in imported_nodes:
                if node.nodeType != node.ELEMENT_NODE:
                    continue
                child = DOM.importNode(document, node, 1)
                parent.appendChild(child)
                child.setAttribute('targetNamespace', namespace)
                attrsNS = imported._attrsNS
                for attrkey in attrsNS.keys():
                    if attrkey[0] == DOM.NS_XMLNS:
                        attr = attrsNS[attrkey].cloneNode(1)
                        child.setAttributeNode(attr)
        finally:
            importdoc.unlink()


class Element:
    """A class that provides common functions for WSDL element classes."""
    def __init__(self, name=None, documentation=''):
        self.name = name
        self.documentation = documentation
        self.extensions = []

    def addExtension(self, item):
        self.extensions.append(item)


class ImportElement(Element):
    def __init__(self, namespace, location):
        self.namespace = namespace
        self.location = location

    _loaded = None


class Types(Collection):
    default = lambda self,k: k.targetNamespace
    def __init__(self, parent):
        Collection.__init__(self, parent)
        self.documentation = ''
        self.extensions = []

    def addSchema(self, schema):
        name = schema.targetNamespace
        self[name] = schema
        return schema

    def addExtension(self, item):
        self.extensions.append(item)


class Message(Element):
    def __init__(self, name, documentation=''):
        Element.__init__(self, name, documentation)
        self.parts = Collection(self)

    def addPart(self, name, type=None, element=None):
        if self.parts.has_key(name):
            raise WSDLError(
                'Duplicate message part element: %s' % name
                )
        if type is None and element is None:
            raise WSDLError(
                'Missing type or element attribute for part: %s' % name
                )
        item = MessagePart(name)
        item.element = element
        item.type = type
        self.parts[name] = item
        return item

    def load(self, elements):
        for element in elements:
            name = DOM.getAttr(element, 'name')
            part = MessagePart(name)
            self.parts[name] = part
            elemref = DOM.getAttr(element, 'element', default=None)
            typeref = DOM.getAttr(element, 'type', default=None)
            if typeref is None and elemref is None:
                raise WSDLError(
                    'No type or element attribute for part: %s' % name
                    )
            if typeref is not None:
                part.type = ParseTypeRef(typeref, element)
            if elemref is not None:
                part.element = ParseTypeRef(elemref, element)


class MessagePart(Element):
    def __init__(self, name):
        Element.__init__(self, name, '')
        self.element = None
        self.type = None


class PortType(Element):
    def __init__(self, name, documentation=''):
        Element.__init__(self, name, documentation)
        self.operations = Collection(self)

    def getWSDL(self):
        return self.parent().parent()

    def addOperation(self, name, documentation='', parameterOrder=None):
        item = Operation(name, documentation, parameterOrder)
        self.operations[name] = item
        return item

    def load(self, elements):
        for element in elements:
            name = DOM.getAttr(element, 'name')
            docs = GetDocumentation(element)
            param_order = DOM.getAttr(element, 'parameterOrder', default=None)
            if param_order is not None:
                param_order = param_order.split(' ')
            operation = self.addOperation(name, docs, param_order)

            item = DOM.getElement(element, 'input', None, None)
            if item is not None:
                name = DOM.getAttr(item, 'name')
                docs = GetDocumentation(item)
                msgref = DOM.getAttr(item, 'message')
                message = msgref.split(':', 1)[-1]
                operation.setInput(message, name, docs)

            item = DOM.getElement(element, 'output', None, None)
            if item is not None:
                name = DOM.getAttr(item, 'name')
                docs = GetDocumentation(item)
                msgref = DOM.getAttr(item, 'message')
                message = msgref.split(':', 1)[-1]
                operation.setOutput(message, name, docs)

            for item in DOM.getElements(element, 'fault', None):
                name = DOM.getAttr(item, 'name')
                docs = GetDocumentation(item)
                msgref = DOM.getAttr(item, 'message')
                message = msgref.split(':', 1)[-1]
                operation.addFault(message, name, docs)


class Operation(Element):
    def __init__(self, name, documentation='', parameterOrder=None):
        Element.__init__(self, name, documentation)
        self.parameterOrder = parameterOrder
        self.faults = Collection(self)
        self.input = None
        self.output = None

    def getPortType(self):
        return self.parent().parent()

    def getInputMessage(self):
        if self.input is None:
            return None
        wsdl = self.getPortType().getWSDL()
        return wsdl.messages[self.input.message]

    def getOutputMessage(self):
        if self.output is None:
            return None
        wsdl = self.getPortType().getWSDL()
        return wsdl.messages[self.output.message]

    def getFaultMessage(self, name):
        wsdl = self.getPortType().getWSDL()
        return wsdl.messages[self.faults[name].message]

    def addFault(self, name, message, documentation=''):
        if self.faults.has_key(name):
            raise WSDLError(
                'Duplicate fault element: %s' % name
                )
        item = MessageRole('fault', message, name, documentation)
        self.faults[name] = item
        return item

    def setInput(self, message, name='', documentation=''):
        self.input = MessageRole('input', message, name, documentation)
        return self.input

    def setOutput(self, message, name='', documentation=''):
        self.output = MessageRole('output', message, name, documentation)
        return self.output


class MessageRole(Element):
    def __init__(self, type, message, name='', documentation=''):
        Element.__init__(self, name, documentation)
        self.message = message
        self.type = type


class Binding(Element):
    def __init__(self, name, type, documentation=''):
        Element.__init__(self, name, documentation)
        self.operations = Collection(self)
        self.type = type

    def getWSDL(self):
        """Return the WSDL object that contains this binding."""
        return self.parent().parent()

    def getPortType(self):
        """Return the PortType object associated with this binding."""
        return self.getWSDL().portTypes[self.type]

    def findBinding(self, kind):
        for item in self.extensions:
            if isinstance(item, kind):
                return item
        return None

    def findBindings(self, kind):
        return [ item for item in self.extensions if isinstance(item, kind) ]

    def addOperationBinding(self, name, documentation=''):
        item = OperationBinding(name, documentation)
        self.operations[name] = item
        return item

    def load(self, elements):
        for element in elements:
            name = DOM.getAttr(element, 'name')
            docs = GetDocumentation(element)
            opbinding = self.addOperationBinding(name, docs)
            opbinding.load_ex(GetExtensions(element))

            item = DOM.getElement(element, 'input', None, None)
            if item is not None:
                mbinding = MessageRoleBinding('input')
                mbinding.documentation = GetDocumentation(item)
                opbinding.input = mbinding
                mbinding.load_ex(GetExtensions(item))

            item = DOM.getElement(element, 'output', None, None)
            if item is not None:
                mbinding = MessageRoleBinding('output')
                mbinding.documentation = GetDocumentation(item)
                opbinding.output = mbinding
                mbinding.load_ex(GetExtensions(item))

            for item in DOM.getElements(element, 'fault', None):
                name = DOM.getAttr(item, 'name')
                mbinding = MessageRoleBinding('fault', name)
                mbinding.documentation = GetDocumentation(item)
                opbinding.faults[name] = mbinding
                mbinding.load_ex(GetExtensions(item))

    def load_ex(self, elements):
        for e in elements:
            ns, name = e.namespaceURI, e.localName
            if ns in DOM.NS_SOAP_BINDING_ALL and name == 'binding':
                transport = DOM.getAttr(e, 'transport', default=None)
                style = DOM.getAttr(e, 'style', default='document')
                ob = SoapBinding(transport, style)
                self.addExtension(ob)
                continue
            elif ns in DOM.NS_HTTP_BINDING_ALL and name == 'binding':
                verb = DOM.getAttr(e, 'verb')
                ob = HttpBinding(verb)
                self.addExtension(ob)
                continue
            else:
                self.addExtension(e)


class OperationBinding(Element):
    def __init__(self, name, documentation=''):
        Element.__init__(self, name, documentation)
        self.input = None
        self.output = None
        self.faults = Collection(self)

    def getBinding(self):
        """Return the parent Binding object of the operation binding."""
        return self.parent().parent()

    def getOperation(self):
        """Return the abstract Operation associated with this binding."""
        return self.getBinding().getPortType().operations[self.name]
        
    def findBinding(self, kind):
        for item in self.extensions:
            if isinstance(item, kind):
                return item
        return None

    def findBindings(self, kind):
        return [ item for item in self.extensions if isinstance(item, kind) ]

    def addInputBinding(self, binding):
        if self.input is None:
            self.input = MessageRoleBinding('input')
        self.input.addExtension(binding)
        return binding

    def addOutputBinding(self, binding):
        if self.output is None:
            self.output = MessageRoleBinding('output')
        self.output.addExtension(binding)
        return binding

    def addFaultBinding(self, name, binding):
        fault = self.get(name, None)
        if fault is None:
            fault = MessageRoleBinding('fault', name)
        fault.addExtension(binding)
        return binding

    def load_ex(self, elements):
        for e in elements:
            ns, name = e.namespaceURI, e.localName
            if ns in DOM.NS_SOAP_BINDING_ALL and name == 'operation':
                soapaction = DOM.getAttr(e, 'soapAction', default=None)
                style = DOM.getAttr(e, 'style', default=None)
                ob = SoapOperationBinding(soapaction, style)
                self.addExtension(ob)
                continue
            elif ns in DOM.NS_HTTP_BINDING_ALL and name == 'operation':
                location = DOM.getAttr(e, 'location')
                ob = HttpOperationBinding(location)
                self.addExtension(ob)
                continue
            else:
                self.addExtension(e)


class MessageRoleBinding(Element):
    def __init__(self, type, name='', documentation=''):
        Element.__init__(self, name, documentation)
        self.type = type

    def findBinding(self, kind):
        for item in self.extensions:
            if isinstance(item, kind):
                return item
        return None

    def findBindings(self, kind):
        return [ item for item in self.extensions if isinstance(item, kind) ]

    def load_ex(self, elements):
        for e in elements:
            ns, name = e.namespaceURI, e.localName
            if ns in DOM.NS_SOAP_BINDING_ALL and name == 'body':
                encstyle = DOM.getAttr(e, 'encodingStyle', default=None)
                namespace = DOM.getAttr(e, 'namespace', default=None)
                parts = DOM.getAttr(e, 'parts', default=None)
                use = DOM.getAttr(e, 'use', default=None)
                if use is None:
                    raise WSDLError(
                        'Invalid soap:body binding element.'
                        )
                ob = SoapBodyBinding(use, namespace, encstyle, parts)
                self.addExtension(ob)
                continue

            elif ns in DOM.NS_SOAP_BINDING_ALL and name == 'fault':
                encstyle = DOM.getAttr(e, 'encodingStyle', default=None)
                namespace = DOM.getAttr(e, 'namespace', default=None)
                name = DOM.getAttr(e, 'name', default=None)
                use = DOM.getAttr(e, 'use', default=None)
                if use is None or name is None:
                    raise WSDLError(
                        'Invalid soap:fault binding element.'
                        )
                ob = SoapFaultBinding(name, use, namespace, encstyle)
                self.addExtension(ob)
                continue

            elif ns in DOM.NS_SOAP_BINDING_ALL and name in (
                'header', 'headerfault'
                ):
                encstyle = DOM.getAttr(e, 'encodingStyle', default=None)
                namespace = DOM.getAttr(e, 'namespace', default=None)
                message = DOM.getAttr(e, 'message')
                part = DOM.getAttr(e, 'part')
                use = DOM.getAttr(e, 'use')
                if name == 'header':
                    _class = SoapHeaderBinding
                else:
                    _class = SoapHeaderFaultBinding
                ob = _class(message, part, use, namespace, encstyle)
                self.addExtension(ob)
                continue

            elif ns in DOM.NS_HTTP_BINDING_ALL and name == 'urlReplacement':
                ob = HttpUrlReplacementBinding()
                self.addExtension(ob)
                continue

            elif ns in DOM.NS_HTTP_BINDING_ALL and name == 'urlEncoded':
                ob = HttpUrlEncodedBinding()
                self.addExtension(ob)
                continue

            elif ns in DOM.NS_MIME_BINDING_ALL and name == 'multipartRelated':
                ob = MimeMultipartRelatedBinding()
                self.addExtension(ob)
                ob.load_ex(GetExtensions(e))
                continue

            elif ns in DOM.NS_MIME_BINDING_ALL and name == 'content':
                part = DOM.getAttr(e, 'part', default=None)
                type = DOM.getAttr(e, 'type', default=None)
                ob = MimeContentBinding(part, type)
                self.addExtension(ob)
                continue

            elif ns in DOM.NS_MIME_BINDING_ALL and name == 'mimeXml':
                part = DOM.getAttr(e, 'part', default=None)
                ob = MimeXmlBinding(part)
                self.addExtension(ob)
                continue

            else:
                self.addExtension(e)


class Service(Element):
    def __init__(self, name, documentation=''):
        Element.__init__(self, name, documentation)
        self.ports = Collection(self)

    def getWSDL(self):
        return self.parent().parent()

    def addPort(self, name, binding, documentation=''):
        item = Port(name, binding, documentation)
        self.ports[name] = item
        return item

    def load(self, elements):
        for element in elements:
            name = DOM.getAttr(element, 'name', default=None)
            docs = GetDocumentation(element)
            binding = DOM.getAttr(element, 'binding', default=None)
            if name is None or binding is None:
                raise WSDLError(
                    'Invalid port element.'
                    )
            binding = binding.split(':', 1)[-1]
            port = self.addPort(name, binding, docs)
            port.load_ex(GetExtensions(element))

    def load_ex(self, elements):
        for e in elements:
            self.addExtension(e)


class Port(Element):
    def __init__(self, name, binding, documentation=''):
        Element.__init__(self, name, documentation)
        self.binding = binding

    def getService(self):
        """Return the Service object associated with this port."""
        return self.parent().parent()

    def getBinding(self):
        """Return the Binding object that is referenced by this port."""
        wsdl = self.getService().getWSDL()
        return wsdl.bindings[self.binding]

    def getPortType(self):
        """Return the PortType object that is referenced by this port."""
        wsdl = self.getService().getWSDL()
        binding = wsdl.bindings[self.binding]
        return wsdl.portTypes[binding.type]

    def getAddressBinding(self):
        """A convenience method to obtain the extension element used
           as the address binding for the port, or None if undefined."""
        for item in self.extensions:
            if isinstance(item, SoapAddressBinding) or \
               isinstance(item, HttpAddressBinding):
                return item
        raise WSDLError(
            'No address binding found in port.'
            )

    def load_ex(self, elements):
        for e in elements:
            ns, name = e.namespaceURI, e.localName
            if ns in DOM.NS_SOAP_BINDING_ALL and name == 'address':
                location = DOM.getAttr(e, 'location', default=None)
                ob = SoapAddressBinding(location)
                self.addExtension(ob)
                continue
            elif ns in DOM.NS_HTTP_BINDING_ALL and name == 'address':
                location = DOM.getAttr(e, 'location', default=None)
                ob = HttpAddressBinding(location)
                self.addExtension(ob)
                continue
            else:
                self.addExtension(e)


class SoapBinding:
    def __init__(self, transport, style='rpc'):
        self.transport = transport
        self.style = style


class SoapAddressBinding:
    def __init__(self, location):
        self.location = location


class SoapOperationBinding:
    def __init__(self, soapAction=None, style=None):
        self.soapAction = soapAction
        self.style = style


class SoapBodyBinding:
    def __init__(self, use, namespace=None, encodingStyle=None, parts=None):
        if not use in ('literal', 'encoded'):
            raise WSDLError(
                'Invalid use attribute value: %s' % use
                )
        self.encodingStyle = encodingStyle
        self.namespace = namespace
        if type(parts) in (type(''), type(u'')):
            parts = parts.split()
        self.parts = parts
        self.use = use

class SoapFaultBinding:
    def __init__(self, name, use, namespace=None, encodingStyle=None):
        if not use in ('literal', 'encoded'):
            raise WSDLError(
                'Invalid use attribute value: %s' % use
                )
        self.encodingStyle = encodingStyle
        self.namespace = namespace
        self.name = name
        self.use = use


class SoapHeaderBinding:
    def __init__(self, message, part, use, namespace=None, encodingStyle=None):
        if not use in ('literal', 'encoded'):
            raise WSDLError(
                'Invalid use attribute value: %s' % use
                )
        self.encodingStyle = encodingStyle
        self.namespace = namespace
        self.message = message
        self.part = part
        self.use = use

    tagname = 'header'

class SoapHeaderFaultBinding(SoapHeaderBinding):
    tagname = 'headerfault'


class HttpBinding:
    def __init__(self, verb):
        self.verb = verb

class HttpAddressBinding:
    def __init__(self, location):
        self.location = location


class HttpOperationBinding:
    def __init__(self, location):
        self.location = location

class HttpUrlReplacementBinding:
    pass


class HttpUrlEncodedBinding:
    pass


class MimeContentBinding:
    def __init__(self, part=None, type=None):
        self.part = part
        self.type = type


class MimeXmlBinding:
    def __init__(self, part=None):
        self.part = part


class MimeMultipartRelatedBinding:
    def __init__(self):
        self.parts = []

    def load_ex(self, elements):
        for e in elements:
            ns, name = e.namespaceURI, e.localName
            if ns in DOM.NS_MIME_BINDING_ALL and name == 'part':
                self.parts.append(MimePartBinding())
                continue


class MimePartBinding:
    def __init__(self):
        self.items = []

    def load_ex(self, elements):
        for e in elements:
            ns, name = e.namespaceURI, e.localName
            if ns in DOM.NS_MIME_BINDING_ALL and name == 'content':
                part = DOM.getAttr(e, 'part', default=None)
                type = DOM.getAttr(e, 'type', default=None)
                ob = MimeContentBinding(part, type)
                self.items.append(ob)
                continue

            elif ns in DOM.NS_MIME_BINDING_ALL and name == 'mimeXml':
                part = DOM.getAttr(e, 'part', default=None)
                ob = MimeXmlBinding(part)
                self.items.append(ob)
                continue

            elif ns in DOM.NS_SOAP_BINDING_ALL and name == 'body':
                encstyle = DOM.getAttr(e, 'encodingStyle', default=None)
                namespace = DOM.getAttr(e, 'namespace', default=None)
                parts = DOM.getAttr(e, 'parts', default=None)
                use = DOM.getAttr(e, 'use', default=None)
                if use is None:
                    raise WSDLError(
                        'Invalid soap:body binding element.'
                        )
                ob = SoapBodyBinding(use, namespace, encstyle, parts)
                self.items.append(ob)
                continue


class WSDLError(Exception):
    pass



def DeclareNSPrefix(writer, prefix, nsuri):
    if writer.hasNSPrefix(nsuri):
        return
    writer.declareNSPrefix(prefix, nsuri)

def ParseTypeRef(value, element):
    parts = value.split(':', 1)
    if len(parts) == 1:
        return (DOM.findTargetNS(element), value)
    nsuri = DOM.findNamespaceURI(parts[0], element)
    return (nsuri, parts[1])

def ParseQName(value, element):
    nameref = value.split(':', 1)
    if len(nameref) == 2:
        nsuri = DOM.findNamespaceURI(nameref[0], element)
        name = nameref[-1]
    else:
        nsuri = DOM.findTargetNS(element)
        name  = nameref[-1]
    return nsuri, name

def GetDocumentation(element):
    docnode = DOM.getElement(element, 'documentation', None, None)
    if docnode is not None:
        return DOM.getElementText(docnode)
    return ''

def GetExtensions(element):
    return [ item for item in DOM.getElements(element, None, None)
        if item.namespaceURI != DOM.NS_WSDL ]

def FindExtensions(object, kind, t_type=type(())):
    if isinstance(kind, t_type):
        result = []
        namespaceURI, name = kind
        return [ item for item in object.extensions
                if hasattr(item, 'nodeType') \
                and DOM.nsUriMatch(namespaceURI, item.namespaceURI) \
                and item.name == name ]
    return [ item for item in object.extensions if isinstance(item, kind) ]

def FindExtension(object, kind, t_type=type(())):
    if isinstance(kind, t_type):
        namespaceURI, name = kind
        for item in object.extensions:
            if hasattr(item, 'nodeType') \
            and DOM.nsUriMatch(namespaceURI, item.namespaceURI) \
            and item.name == name:
                return item
    else:
        for item in object.extensions:
            if isinstance(item, kind):
                return item
    return None


class SOAPCallInfo:
    """SOAPCallInfo captures the important binding information about a 
       SOAP operation, in a structure that is easier to work with than
       raw WSDL structures."""

    def __init__(self, methodName):
        self.methodName = methodName
        self.inheaders = []
        self.outheaders = []
        self.inparams = []
        self.outparams = []
        self.retval = None

    encodingStyle = DOM.NS_SOAP_ENC
    documentation = ''
    soapAction = None
    transport = None
    namespace = None
    location = None
    use = 'encoded'
    style = 'rpc'

    def addInParameter(self, name, type, namespace=None, element_type=0):
        """Add an input parameter description to the call info."""
        parameter = ParameterInfo(name, type, namespace, element_type)
        self.inparams.append(parameter)
        return parameter

    def addOutParameter(self, name, type, namespace=None, element_type=0):
        """Add an output parameter description to the call info."""
        parameter = ParameterInfo(name, type, namespace, element_type)
        self.outparams.append(parameter)
        return parameter

    def setReturnParameter(self, name, type, namespace=None, element_type=0):
        """Set the return parameter description for the call info."""
        parameter = ParameterInfo(name, type, namespace, element_type)
        self.retval = parameter
        return parameter

    def addInHeaderInfo(self, name, type, namespace, element_type=0,
                        mustUnderstand=0):
        """Add an input SOAP header description to the call info."""
        headerinfo = HeaderInfo(name, type, namespace, element_type)
        if mustUnderstand:
            headerinfo.mustUnderstand = 1
        self.inheaders.append(headerinfo)
        return headerinfo

    def addOutHeaderInfo(self, name, type, namespace, element_type=0,
                         mustUnderstand=0):
        """Add an output SOAP header description to the call info."""
        headerinfo = HeaderInfo(name, type, namespace, element_type)
        if mustUnderstand:
            headerinfo.mustUnderstand = 1
        self.outheaders.append(headerinfo)
        return headerinfo

    def getInParameters(self):
        """Return a sequence of the in parameters of the method."""
        return self.inparams

    def getOutParameters(self):
        """Return a sequence of the out parameters of the method."""
        return self.outparams

    def getReturnParameter(self):
        """Return param info about the return value of the method."""
        return self.retval

    def getInHeaders(self):
        """Return a sequence of the in headers of the method."""
        return self.inheaders

    def getOutHeaders(self):
        """Return a sequence of the out headers of the method."""
        return self.outheaders


class ParameterInfo:
    """A ParameterInfo object captures parameter binding information."""
    def __init__(self, name, type, namespace=None, element_type=0):
        if element_type:
            self.element_type = 1
        if namespace is not None:
            self.namespace = namespace
        self.name = name
        self.type = type

    element_type = 0
    namespace = None
    default = None


class HeaderInfo(ParameterInfo):
    """A HeaderInfo object captures SOAP header binding information."""
    def __init__(self, name, type, namespace, element_type=None):
        ParameterInfo.__init__(self, name, type, namespace, element_type)

    mustUnderstand = 0
    actor = None


def callInfoFromWSDL(port, name):
    """Return a SOAPCallInfo given a WSDL port and operation name."""
    wsdl = port.getService().getWSDL()
    binding = port.getBinding()
    portType = binding.getPortType()
    operation = portType.operations[name]
    opbinding = binding.operations[name]
    messages = wsdl.messages
    callinfo = SOAPCallInfo(name)

    addrbinding = port.getAddressBinding()
    if not isinstance(addrbinding, SoapAddressBinding):
        raise ValueError, 'Unsupported binding type.'        
    callinfo.location = addrbinding.location

    soapbinding = binding.findBinding(SoapBinding)
    if soapbinding is None:
        raise ValueError, 'Missing soap:binding element.'
    callinfo.transport = soapbinding.transport
    callinfo.style = soapbinding.style or 'document'

    soap_op_binding = opbinding.findBinding(SoapOperationBinding)
    if soap_op_binding is not None:
        callinfo.soapAction = soap_op_binding.soapAction
        callinfo.style = soap_op_binding.style or callinfo.style

    parameterOrder = operation.parameterOrder

    if operation.input is not None:
        message = messages[operation.input.message]
        msgrole = opbinding.input

        mime = msgrole.findBinding(MimeMultipartRelatedBinding)
        if mime is not None:
            raise ValueError, 'Mime bindings are not supported.'
        else:
            for item in msgrole.findBindings(SoapHeaderBinding):
                part = messages[item.message].parts[item.part]
                header = callinfo.addInHeaderInfo(
                    part.name,
                    part.element or part.type,
                    item.namespace,
                    element_type = part.element and 1 or 0
                    )
                header.encodingStyle = item.encodingStyle

            body = msgrole.findBinding(SoapBodyBinding)
            if body is None:
                raise ValueError, 'Missing soap:body binding.'
            callinfo.encodingStyle = body.encodingStyle
            callinfo.namespace = body.namespace
            callinfo.use = body.use

            if body.parts is not None:
                parts = []
                for name in body.parts:
                    parts.append(message.parts[name])
            else:
                parts = message.parts.values()

            for part in parts:
                callinfo.addInParameter(
                    part.name,
                    part.element or part.type,
                    element_type = part.element and 1 or 0
                    )

    if operation.output is not None:
        try:
            message = messages[operation.output.message]
        except KeyError:
            if self.strict:
                raise RuntimeError(
                    "Recieved message not defined in the WSDL schema: %s" %
                    operation.output.message)
            else:
                message = wsdl.addMessage(operation.output.message)
                print "Warning:", \
                      "Recieved message not defined in the WSDL schema.", \
                      "Adding it."
                print "Message:", operation.output.message
         
        msgrole = opbinding.output

        mime = msgrole.findBinding(MimeMultipartRelatedBinding)
        if mime is not None:
            raise ValueError, 'Mime bindings are not supported.'
        else:
            for item in msgrole.findBindings(SoapHeaderBinding):
                part = messages[item.message].parts[item.part]
                header = callinfo.addOutHeaderInfo(
                    part.name,
                    part.element or part.type,
                    item.namespace,
                    element_type = part.element and 1 or 0
                    )
                header.encodingStyle = item.encodingStyle

            body = msgrole.findBinding(SoapBodyBinding)
            if body is None:
                raise ValueError, 'Missing soap:body binding.'
            callinfo.encodingStyle = body.encodingStyle
            callinfo.namespace = body.namespace
            callinfo.use = body.use

            if body.parts is not None:
                parts = []
                for name in body.parts:
                    parts.append(message.parts[name])
            else:
                parts = message.parts.values()

            if parts:
                callinfo.setReturnParameter(
                    parts[0].name,
                    parts[0].element or parts[0].type,
                    element_type = parts[0].element and 1 or 0
                    )
                for part in parts[1:]:
                    callinfo.addOutParameter(
                        part.name,
                        part.element or part.type,
                        element_type = part.element and 1 or 0
                        )

    return callinfo
