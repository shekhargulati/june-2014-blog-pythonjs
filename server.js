#!/usr/bin/env node
var fs = require('fs')
var pythonjs = require('python-js')
var pycode = fs.readFileSync( './app.py', {'encoding':'utf8'} )
var jscode = pythonjs.translator.to_javascript( pycode )
eval( pythonjs.runtime.javascript + jscode )