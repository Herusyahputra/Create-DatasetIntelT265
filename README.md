# Create-DatasetIntelT265

## Create dataset visual Odometry using camera Intel T-625

Date: December 29, 2021                                                                                                                                                                  
Name Project: Create Dataset Using Intel T265



**1. Introduction**                                                                                
This program was created to make it easier to capture datasets (Image Sequence) and Poses (Ground Truth) from Stereo cameras and Inertial Measurement Units (IMUs) from Intel T265 cameras.

**2. Requirements**
   - Create Folder in your directory (IntelL & IntelR)

**3. How to used**                                                                                  
   - Follow these steps to run                                                                
   - Open your terminal by clicking Ctrl + Alt + T
   
   ```
   $ git clone https://github.com/MoilOrg/create-dataset-intel-t-625.git
   ```
   ```
   $ cd create-dataset-intel-t-625/
   ```
   - Create Virtual Environment
   ```
   $ virtualenv env
   ```
   ```
   $ source env/bin/activate
   ```
   - Doing the Installation requirements
   ```
   $ pip install -r requirements.txt
   ```
   - Connected the camera Intel T265 in your computer 
   - Run the program
   ```
   $ python main.py
   ```

 **4. Result**
   
   ![a](https://user-images.githubusercontent.com/60929939/148066663-ad1e7327-b8b9-4cd2-a00b-9809835d1bb5.png)

