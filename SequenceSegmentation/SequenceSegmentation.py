import os
import numpy
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

class SequenceSegmentation(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Sequence Segmentation"
        self.parent.categories = ["4D Ultrasound"]
        self.parent.dependencies = []
        self.parent.contributors = ["Denis Corbin"]
        self.parent.helpText = """
            This module creates segmentations from sequence data.
            """
        self.parent.acknowledgementText = """
            Thanks to everyone.
            """

class SequenceSegmentationWidget(ScriptedLoadableModuleWidget):
    def __init__(self, parent=None):
        ScriptedLoadableModuleWidget.__init__(self, parent)

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        
        # Create a button
        loadButton = qt.QPushButton("Run Segmentation")
        self.layout.addWidget(loadButton)
        loadButton.connect('clicked(bool)', self.onLoadButton)

        # Add input path selector
        self.inputSelector = ctk.ctkPathLineEdit()
        self.inputSelector.filters = ctk.ctkPathLineEdit.Files
        self.inputSelector.nameFilters = ["Sequence files (*.seq.nrrd)"]
        self.layout.addWidget(self.inputSelector)
        
        # Add vertical spacer
        self.layout.addStretch(1)

    def onLoadButton(self):
        logic = SequenceSegmentationLogic()
        logic.run(self.inputSelector.currentPath)

class SequenceSegmentationLogic(ScriptedLoadableModuleLogic):
    def run(self, sequenceFilePath):
        # Your existing code goes here
        slicer.mrmlScene.Clear()
        sequenceNode = slicer.util.loadSequence(sequenceFilePath)

        # Extract the base filename without extension and path
        baseFileName = os.path.basename(sequenceFilePath)
        # Remove the '.dcm_.seq.nrrd' suffix
        baseFileName = baseFileName.replace('.dcm_.seq.nrrd', '')

        # Construct the mask directory path (assuming it's in the same directory)
        maskDir = os.path.dirname(sequenceFilePath)
        sequenceBrowserNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSequenceBrowserNode")

        # Get the master volume node (proxy node) from the sequence browser
        masterVolumeNode = sequenceBrowserNode.GetProxyNode(sequenceBrowserNode.GetMasterSequenceNode())

        # Create a new segmentation node and initialize it
        segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
        segmentationNode.SetName("SegmentationNode - Do not use")
        segmentationNode.CreateDefaultDisplayNodes()

        # Create a sequence node for the segmentation
        segmentationSequenceNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSequenceNode")
        segmentationSequenceNode.SetName("SegmentationSequence")

        # Add the segmentation sequence to the browser node
        sequenceBrowserNode.AddSynchronizedSequenceNode(segmentationSequenceNode)

        # Add the segmentation node as a proxy node
        sequenceBrowserNode.AddProxyNode(segmentationNode, segmentationSequenceNode)
        sequenceBrowserNode.SetSaveChanges(segmentationSequenceNode, True)

        # Get number of items in sequence
        numberOfFrames = sequenceNode.GetNumberOfDataNodes()

        # Create Segment Editor
        segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
        segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
        segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
        segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)

        # Process each frame
        for frameIndex in range(numberOfFrames):
            # Move to current frame
            sequenceBrowserNode.SetSelectedItemNumber(frameIndex)
            
            # Get the proxy segmentation node
            proxySegmentationNode = sequenceBrowserNode.GetProxyNode(segmentationSequenceNode)
            proxySegmentationNode.CreateDefaultDisplayNodes()
            
            # Enable 3D display
            displayNode = proxySegmentationNode.GetDisplayNode()
            displayNode.SetVisibility3D(True)
            
            # Construct filename for current frame
            maskFileName = os.path.join(maskDir, f"val_{baseFileName}_{frameIndex:03d}_ensemble.nii.gz")
            
            # Load the .nii.gz file
            labelVolume = slicer.util.loadVolume(maskFileName)
            
            # Setup segment editor for current frame
            segmentEditorWidget.setSegmentationNode(proxySegmentationNode)
            segmentEditorWidget.setSourceVolumeNode(labelVolume)
            
            # Get label volume array
            labelArray = slicer.util.arrayFromVolume(labelVolume)
            
            # Find unique labels
            uniqueLabels = numpy.unique(labelArray)
            uniqueLabels = uniqueLabels[uniqueLabels != 0]  # Exclude background
            
            # Create a segment for each label
            for labelValue in uniqueLabels:
                segmentName = f"Segment_{labelValue}"
                
                # Check if segment already exists
                if not proxySegmentationNode.GetSegmentation().GetSegmentIdBySegmentName(segmentName):
                    # Add empty segment only if it doesn't exist
                    proxySegmentationNode.GetSegmentation().AddEmptySegment(segmentName)
                
                # Select the current segment
                segmentEditorWidget.setCurrentSegmentID(proxySegmentationNode.GetSegmentation().GetSegmentIdBySegmentName(segmentName))
                
                # Use "Threshold" effect to create the segment
                segmentEditorWidget.setActiveEffectByName("Threshold")
                effect = segmentEditorWidget.activeEffect()
                effect.setParameter("MinimumThreshold", str(labelValue))
                effect.setParameter("MaximumThreshold", str(labelValue))
                effect.self().onApply()
                
                # Show 3D for the current segment
                segmentID = proxySegmentationNode.GetSegmentation().GetSegmentIdBySegmentName(segmentName)
                displayNode.SetSegmentVisibility3D(segmentID, True)
            
            # Clean up current frame's label volume
            slicer.mrmlScene.RemoveNode(labelVolume)

        # Final cleanup
        slicer.mrmlScene.RemoveNode(segmentEditorNode)
        slicer.mrmlScene.RemoveNode(segmentationNode)