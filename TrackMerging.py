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

    mu_plus_data = df_mu_plus.AsNumpy(["fpgaTriggers","nimTriggers", "runID", "spillID", "eventID", "rfID","turnID", "rfIntensities", "elementIDs", "detectorIDs", "driftDistances","tdcTimes", "hitsInTime"])
    mu_minus_data = df_mu_minus.AsNumpy(["fpgaTriggers","nimTriggers", "runID", "spillID", "eventID", "rfID","turnID", "rfIntensities", "elementIDs", "detectorIDs", "driftDistances","tdcTimes", "hitsInTime"])

    # Create the output file and TTree
    output_file = ROOT.TFile(output_file_path, "RECREATE")
    output_tree = ROOT.TTree("tree", "Selected Muons")

    # Define branches for the output tree
    runID = np.zeros(1, dtype=int)
    spillID = np.zeros(1, dtype=int)
    eventID = np.zeros(1, dtype=int)

    fpgaTriggers = np.zeros(5, dtype=int)
    nimTriggers = np.zeros(5, dtype=int)
    rfIntensities = np.full(33, 10000, dtype=int)

    elementIDs = ROOT.std.vector('int')()
    detectorIDs = ROOT.std.vector('int')()
    driftDistances = ROOT.std.vector('double')()
    tdcTimes = ROOT.std.vector('double')()
    hitsInTime = ROOT.std.vector('bool')()

    triggerElementIDs = ROOT.std.vector('int')()
    triggerDetectorIDs = ROOT.std.vector('int')()
    triggerDriftDistances = ROOT.std.vector('double')()
    triggerTdcTimes = ROOT.std.vector('double')()
    triggerHitsInTime = ROOT.std.vector('bool')()

    output_tree.Branch("runID", runID, "runID/I")
    output_tree.Branch("spillID", spillID, "spillID/I")
    output_tree.Branch("eventID", eventID, "eventID/I")
    output_tree.Branch("fpgaTriggers", fpgaTriggers, "fpgaTriggers[5]/I")
    output_tree.Branch("nimTriggers",nimTriggers, "nimTriggers[5]/I")
    output_tree.Branch("rfIntensities",rfIntensities, "rfIntensities[33]/I")

    output_tree.Branch("elementIDs", elementIDs)
    output_tree.Branch("detectorIDs", detectorIDs)
    output_tree.Branch("driftDistances", driftDistances)
    output_tree.Branch("tdcTimes", tdcTimes)
    output_tree.Branch("hitsInTime", hitsInTime)

    output_tree.Branch("triggerElementIDs", triggerElementIDs)
    output_tree.Branch("triggerDetectorIDs", triggerDetectorIDs)
    output_tree.Branch("triggerDriftDistances", triggerDriftDistances)
    output_tree.Branch("triggerTdcTimes", triggerTdcTimes)
    output_tree.Branch("triggerHitsInTime", triggerHitsInTime)

    # Event loop for combining single tracks
    mu_plus_events = len(mu_plus_data["runID"])
    mu_minus_events = len(mu_minus_data["runID"])

    for i in range(desired_number_of_events):
        mu_plus_index = random.randint(0, mu_plus_events - 1)
        mu_minus_index = random.randint(0, mu_minus_events - 1)

        # Fill event data
        runID[0] = mu_plus_data["runID"][mu_plus_index]
        spillID[0] = mu_plus_data["spillID"][mu_plus_index]
        eventID[0] = mu_plus_data["eventID"][mu_plus_index]

        fpgaTriggers[0] = 1
        fpgaTriggers[1] = 1
        fpgaTriggers[2] = 1
        fpgaTriggers[3] = 1
        fpgaTriggers[4] = 1

        elementIDs.clear()
        detectorIDs.clear()
        driftDistances.clear()
        tdcTimes.clear()
        hitsInTime.clear()

        triggerElementIDs.clear()
        triggerDetectorIDs.clear()
        triggerDriftDistances.clear()
        triggerTdcTimes.clear()
        triggerHitsInTime.clear()
        
        # mu+ tracks
        for j in range(len(mu_plus_data["elementIDs"][mu_plus_index])):
            elementIDs.push_back(mu_plus_data["elementIDs"][mu_plus_index][j])
            detectorIDs.push_back(mu_plus_data["detectorIDs"][mu_plus_index][j])
            tdcTimes.push_back(mu_plus_data["tdcTimes"][mu_plus_index][j])
            driftDistances.push_back(mu_plus_data["driftDistances"][mu_plus_index][j])
            hitsInTime.push_back(1)

        # mu- tracks
        for j in range(len(mu_minus_data["elementIDs"][mu_minus_index])):
            elementIDs.push_back(mu_minus_data["elementIDs"][mu_minus_index][j])
            detectorIDs.push_back(mu_minus_data["detectorIDs"][mu_minus_index][j])
            tdcTimes.push_back(mu_minus_data["tdcTimes"][mu_minus_index][j])
            driftDistances.push_back(mu_minus_data["driftDistances"][mu_minus_index][j])
            hitsInTime.push_back(1)


        # mu+ tracks
        for j in range(len(mu_plus_data["elementIDs"][mu_plus_index])):
            triggerDetectorIDs.push_back(mu_plus_data["elementIDs"][mu_plus_index][j])
            triggerElementIDs.push_back(mu_plus_data["detectorIDs"][mu_plus_index][j])
            triggerTdcTimes.push_back(mu_plus_data["tdcTimes"][mu_plus_index][j])
            triggerDriftDistances.push_back(mu_plus_data["driftDistances"][mu_plus_index][j])
            triggerHitsInTime.push_back(1)

        # mu- tracks

        for j in range(len(mu_minus_data["elementIDs"][mu_minus_index])):
            triggerDetectorIDs.push_back(mu_minus_data["elementIDs"][mu_minus_index][j])
            triggerElementIDs.push_back(mu_minus_data["detectorIDs"][mu_minus_index][j])
            triggerTdcTimes.push_back(int(mu_minus_data["tdcTimes"][mu_minus_index][j]))
            triggerDriftDistances.push_back(int(mu_minus_data["driftDistances"][mu_minus_index][j]))
            triggerHitsInTime.push_back(1)

        output_tree.Fill()

    output_file.Write()
    output_file.Close()
    print(f"Output file created: {output_file_path}")

mu_plus_file = "data/Vector-In-Mup.root"
mu_minus_file = "data/Vector-In-Mum.root"
output_file = "data/combined_tracks.root"
desired_events = 10000
main(mu_plus_file, mu_minus_file, output_file, desired_events)
