import commands
proyecto='eliminarsigpuntuacion.py'
#proyecto='scrapConsortium.py'
print proyecto
#a=commands.getoutput('python proyectoScrapy/codigoscrap/'+proyecto)
status, output=commands.getstatusoutput('python proyectoScrapy/codigoscrap/'+proyecto)
print status
print output
