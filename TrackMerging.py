import ROOT
import random
import numpy as np

def main(mu_plus_file_path, mu_minus_file_path, output_file_path, desired_number_of_events):
    # Open the simulated input files
    mu_plus_file = ROOT.TFile.Open(mu_plus_file_path)
    mu_minus_file = ROOT.TFile.Open(mu_minus_file_path)
    
    if not mu_plus_file or mu_plus_file.IsZombie():
        print(f"Error: Could not open mu+ input file {mu_plus_file_path}!")
        return
    if not mu_minus_file or mu_minus_file.IsZombie():
        print(f"Error: Could not open mu- input file {mu_minus_file_path}!")
        return

    # Create RDataFrame for both input trees
    df_mu_plus = ROOT.RDataFrame("tree", mu_plus_file_path)
    df_mu_minus = ROOT.RDataFrame("tree", mu_minus_file_path)

    mu_plus_data = df_mu_plus.AsNumpy(["trig_bits" ,"RunID", "SpillID", "EventID", "track_px", "track_py", 
                                       "track_pz", "track_x", "track_y", "track_z", 
                                       "track_charge", "elementID", "detectorID", "driftDistance","tdcTime"])
    mu_minus_data = df_mu_minus.AsNumpy(["trig_bits", "RunID", "SpillID", "EventID", "track_px", "track_py", 
                                         "track_pz", "track_x", "track_y", "track_z", 
                                         "track_charge", "elementID", "detectorID", "driftDistance","tdcTime"])

    # Create the output file and TTree
    output_file = ROOT.TFile(output_file_path, "RECREATE")
    output_tree = ROOT.TTree("tree", "Selected Muons")

    # Define branches for the output tree
    RunID = np.zeros(1, dtype=int)
    SpillID = np.zeros(1, dtype=int)
    EventID = np.zeros(1, dtype=int)
    track_multiplicity = np.zeros(1, dtype=int)

    fpga_triggers = np.zeros(5, dtype=int)
    nim_triggers = np.zeros(5, dtype=int)

    track_px = ROOT.std.vector('float')()
    track_py = ROOT.std.vector('float')()
    track_pz = ROOT.std.vector('float')()
    track_x = ROOT.std.vector('float')()
    track_y = ROOT.std.vector('float')()
    track_z = ROOT.std.vector('float')()

    track_charge = ROOT.std.vector('int')()
    ElementID = ROOT.std.vector('int')()
    DetectorID = ROOT.std.vector('int')()
    DriftDistance = ROOT.std.vector('float')()
    TdcTime = ROOT.std.vector('float')()

    output_tree.Branch("RunID", RunID, "RunID/I")
    output_tree.Branch("SpillID", SpillID, "SpillID/I")
    output_tree.Branch("EventID", EventID, "EventID/I")
    output_tree.Branch("track_multiplicity", track_multiplicity, "track_multiplicity/I")
    output_tree.Branch("fpga_triggers", fpga_triggers, "fpga_triggers[5]/I")
    output_tree.Branch("nim_triggers",nim_triggers, "nim_triggers[5]/I")


    output_tree.Branch("track_px", track_px)
    output_tree.Branch("track_py", track_py)
    output_tree.Branch("track_pz", track_pz)
    output_tree.Branch("track_x", track_x)
    output_tree.Branch("track_y", track_y)
    output_tree.Branch("track_z", track_z)
    output_tree.Branch("track_charge", track_charge)
    output_tree.Branch("ElementID", ElementID)
    output_tree.Branch("DetectorID", DetectorID)
    output_tree.Branch("DriftDistance", DriftDistance)
    output_tree.Branch("TdcTime", TdcTime)

    # Event loop for combining single tracks
    mu_plus_events = len(mu_plus_data["RunID"])
    mu_minus_events = len(mu_minus_data["RunID"])

    for i in range(desired_number_of_events):
        mu_plus_index = random.randint(0, mu_plus_events - 1)
        mu_minus_index = random.randint(0, mu_minus_events - 1)

        # Fill event data
        RunID[0] = mu_plus_data["RunID"][mu_plus_index]
        SpillID[0] = mu_plus_data["SpillID"][mu_plus_index]
        EventID[0] = mu_plus_data["EventID"][mu_plus_index]
        track_multiplicity[0] = len(mu_plus_data["track_px"][mu_plus_index]) + len(mu_minus_data["track_px"][mu_minus_index])
        fpga_triggers[0] = 1
        fpga_triggers[1] = 1
        fpga_triggers[2] = 1
        fpga_triggers[3] = 1
        fpga_triggers[4] = 1

        # Clear vector branches
        track_px.clear()
        track_py.clear()
        track_pz.clear()
        track_x.clear()
        track_y.clear()
        track_z.clear()
        track_charge.clear()
        ElementID.clear()
        DetectorID.clear()
        DriftDistance.clear()
        TdcTime.clear()
        
        #mu+ tracks
        for j in range(len(mu_plus_data["track_px"][mu_plus_index])):
            track_px.push_back(mu_plus_data["track_px"][mu_plus_index][j])
            track_py.push_back(mu_plus_data["track_py"][mu_plus_index][j])
            track_pz.push_back(mu_plus_data["track_pz"][mu_plus_index][j])
            track_x.push_back(mu_plus_data["track_x"][mu_plus_index][j])
            track_y.push_back(mu_plus_data["track_y"][mu_plus_index][j])
            track_z.push_back(mu_plus_data["track_z"][mu_plus_index][j])
            track_charge.push_back(mu_plus_data["track_charge"][mu_plus_index][j])
        #mu- tracks
        for j in range(len(mu_minus_data["track_px"][mu_minus_index])):
            track_px.push_back(mu_minus_data["track_px"][mu_minus_index][j])
            track_py.push_back(mu_minus_data["track_py"][mu_minus_index][j])
            track_pz.push_back(mu_minus_data["track_pz"][mu_minus_index][j])
            track_x.push_back(mu_minus_data["track_x"][mu_minus_index][j])
            track_y.push_back(mu_minus_data["track_y"][mu_minus_index][j])
            track_z.push_back(mu_minus_data["track_z"][mu_minus_index][j])
            track_charge.push_back(mu_minus_data["track_charge"][mu_minus_index][j])


                # mu+ tracks
        for j in range(len(mu_plus_data["elementID"][mu_plus_index])):
            ElementID.push_back(mu_plus_data["elementID"][mu_plus_index][j])
            DetectorID.push_back(mu_plus_data["detectorID"][mu_plus_index][j])
            TdcTime.push_back(int(mu_plus_data["tdcTime"][mu_plus_index][j]))
            DriftDistance.push_back(int(mu_plus_data["driftDistance"][mu_plus_index][j]))

        # mu- tracks
        for j in range(len(mu_minus_data["elementID"][mu_minus_index])):
            ElementID.push_back(mu_minus_data["elementID"][mu_minus_index][j])
            DetectorID.push_back(mu_minus_data["detectorID"][mu_minus_index][j])
            TdcTime.push_back(int(mu_minus_data["tdcTime"][mu_minus_index][j]))
            DriftDistance.push_back(int(mu_minus_data["driftDistance"][mu_minus_index][j]))


        output_tree.Fill()

    output_file.Write()
    output_file.Close()
    print(f"Output file created: {output_file_path}")

mu_plus_file = "data/sim/sim_dump_mup.root"
mu_minus_file = "data/sim/sim_dump_mum.root"
output_file = "data/combined_tracks.root"
desired_events = 5000
main(mu_plus_file, mu_minus_file, output_file, desired_events)
