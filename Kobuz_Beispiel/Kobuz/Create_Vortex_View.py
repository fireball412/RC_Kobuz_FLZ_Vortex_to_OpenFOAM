from paraview.simple import *
from pathlib import Path
root=Path(__file__).resolve().parent
reader=OpenFOAMReader(registrationName='Airflow volume',FileName=str(root/'Kobuz.foam'))
reader.MeshRegions=['internalMesh']
reader.CellArrays=['U','p']
reader.UpdatePipelineInformation()
time=max(reader.TimestepValues)
reader.UpdatePipeline(time)
gradient=Gradient(registrationName='Vorticity and Q criterion',Input=reader)
gradient.ScalarArray=['CELLS','U']
gradient.ComputeGradient=0
gradient.ComputeVorticity=1
gradient.ComputeQCriterion=1
gradient.VorticityArrayName='Vorticity'
gradient.QCriterionArrayName='QCriterion'
gradient.UpdatePipeline(time)
points=CellDatatoPointData(registrationName='Smooth vortex field',Input=gradient)
points.UpdatePipeline(time)
contour=Contour(registrationName='Vortex surfaces — adjust Q threshold',Input=points)
contour.ContourBy=['POINTS','QCriterion']
contour.Isosurfaces=[50.0]
contour.UpdatePipeline(time)
wing=OpenFOAMReader(registrationName='Aircraft surfaces',FileName=str(root/'Kobuz.foam'))
wing.MeshRegions=['patch/kobuz']
wing.CellArrays=['p']
wing.UpdatePipeline(time)
view=GetActiveViewOrCreate('RenderView')
view.ViewTime=time
view.ViewSize=[1400,850]
view.Background=[0.08,0.11,0.15]
view.UseColorPaletteForBackground=0
body=Show(wing,view)
body.Representation='Surface'
ColorBy(body,None)
body.DiffuseColor=[0.72,0.75,0.79]
vortices=Show(contour,view)
vortices.Representation='Surface'
ColorBy(vortices,('POINTS','Vorticity','Magnitude'))
vortices.RescaleTransferFunctionToDataRange(True,False)
vortices.SetScalarBarVisibility(view,True)
lookup=GetColorTransferFunction('Vorticity')
lookup.RescaleTransferFunction(0,500)
vortices.Opacity=0.65
bar=GetScalarBar(lookup,view)
bar.Title='Vorticity';bar.ComponentTitle='Magnitude (1/s)'
view.CameraPosition=[3.9,-5.8,3.1]
view.CameraFocalPoint=[1.0,0.0,0.08]
view.CameraViewUp=[0,0,1]
view.CameraParallelProjection=1
view.CameraParallelScale=1.65
GetAnimationScene().AnimationTime=time
SetActiveSource(contour)
Render(view)
SaveState(str(root/'Kobuz_Vortices.pvsm'))
SaveScreenshot(str(root/'Kobuz_Vortices.png'),view,ImageResolution=[1400,850])
print('Final step:',time,'Vortex surface cells:',contour.GetDataInformation().GetNumberOfCells())
