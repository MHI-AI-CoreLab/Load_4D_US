# Sequence Segmentation Module for 3D Slicer

## Description
This custom 3D Slicer module processes sequence data (4D images) and creates corresponding segmentations using pre-existing mask files. It automatically creates segments for each unique label in the mask files and adds them to a sequence.

## Installation

### 1. Module Installation
1. Open 3D Slicer
2. Go to Developer Tools > Extension Wizard
3. Select Extension
4. Chose the directory LOAD_4D_US
5. Click yes when prompted if you want to load the module

### 2. File Structure Requirements
Your data should be organized as follows (flat directory):
```
YourDataDirectory/
│
├── sequence_file.dcm_.seq.nrrd    # Your 4D sequence file
│
├── val_sequence_file_000_ensemble.nii.gz    # Mask for frame 0
├── val_sequence_file_001_ensemble.nii.gz    # Mask for frame 1
├── val_sequence_file_002_ensemble.nii.gz    # Mask for frame 2
└── ...                                      # Additional frame masks
```

#### Naming Convention
- Sequence file: Can have any name but must end with `.dcm_.seq.nrrd`
- Mask files must follow this pattern:
  - `val_[original_filename]_[frame_number]_ensemble.nii.gz`
  - Frame numbers must be three digits (e.g., 000, 001, 002)
  - Must be in the same directory as the sequence file

## Usage

1. Open 3D Slicer
2. Find the module:
   - Click on the "Modules" dropdown menu
   - Search for "Sequence Segmentation"
   - Or find it in the "Examples" category

3. Using the Module:
   - Use the file browser to select your sequence file
   - Click "Run Segmentation"
   - Wait for processing to complete
   - The resulting segmentation sequence will be automatically loaded

## Expected Input/Output

### Input
- A 4D sequence file (`.dcm_.seq.nrrd`)
- Corresponding mask files (`.nii.gz`) for each frame

### Output
- A segmentation sequence with:
  - Individual segments for each unique label
  - 3D visualization enabled
  - Synchronized with the original sequence

## Troubleshooting

Common issues and solutions:

1. **Module not appearing in Slicer:**
   - Verify the file is in the correct modules directory
   - Check for Python syntax errors
   - Restart Slicer

2. **Processing fails:**
   - Ensure mask files follow the exact naming convention
   - Verify all mask files exist for each frame
   - Check file permissions

3. **Missing mask files:**
   - The module expects a mask file for every frame
   - Verify mask file naming matches the sequence file name

## Requirements
- 3D Slicer (version 4.11 or later)
- Sufficient disk space for processing
- All required mask files must be present

## Additional Notes
- Processing time depends on:
  - Number of frames
  - Image size
  - Number of unique labels
- The module will clear the scene before processing
- Progress can be monitored via the progress bar
- Processing can be cancelled at any time

## Support
For issues or questions:
- Check the 3D Slicer forum
- Report issues on the project repository
- Contact the module maintainer

## License
[Add your license information here]

## Contributors
[Add contributor information here]

## Version History
- 1.0.0: Initial release
  - Basic sequence processing
  - Automatic segmentation creation
  - Progress monitoring