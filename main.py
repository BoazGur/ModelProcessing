import os
from FileReader import FileReader
from ProcessModel import ProcessModelParser
from Converter import CsvConverter, XesConverter
from ProcessDiscovery import ProcessDiscovery

def main():
    input_dir = "logs_txt/"
    output_dir = "outputs/"
    os.makedirs(output_dir, exist_ok=True)

    file_reader = FileReader(input_dir, portion=1)
    parser = ProcessModelParser()

    for i, line in enumerate(file_reader.read_files_chunks()):
        if i == 0:
            parser.parse_headers(line)
        else:
            event_priority, event_type, event_outcome, event_server = parser.parse_line(line)
            if event_priority and event_type and event_outcome:
                parser.add_event(event_priority)
                parser.add_event(event_type)
                parser.add_event(event_outcome)
            
            if event_server:
                parser.add_event(event_server)

    process_model = parser.get_model()

    csv_converter = CsvConverter()
    csv_path = os.path.join(output_dir, "process_model.csv")
    csv_converter.convert(csv_path, process_model)
    print(f"CSV file exported to {csv_path}")

    xes_converter = XesConverter()
    xes_path = os.path.join(output_dir, "process_model.xes")
    xes_converter.convert(xes_path, process_model)
    print(f"XES file exported to {xes_path}")

    process_discovery = ProcessDiscovery()
    process_discovery.import_log(xes_path)
    process_discovery.split_log(split_ratio = 0.5)

    algorithms = ['alpha', 'inductive', 'heuristics']
    for algo in algorithms:
        algo_output_dir = os.path.join(output_dir, f"{algo}_miner")
        os.makedirs(algo_output_dir, exist_ok=True)
        
        process_discovery.discover_process(algorithm=algo)
        
        process_discovery.plot_petri_net(os.path.join(algo_output_dir, "petri_net.png"))
        process_discovery.plot_reachability_graph(os.path.join(algo_output_dir, "reachability_graph.png"))
        process_discovery.plot_transition_system(os.path.join(algo_output_dir, "transition_system.png"))
        process_discovery.visualize_markings(os.path.join(algo_output_dir, "markings.png"))

        conformance_results = process_discovery.perform_conformance_checking()
        process_discovery.visualize_conformance(conformance_results, os.path.join(algo_output_dir, "conformance_metrics.png"))

        print(f"Analysis completed for {algo} miner. Results saved in {algo_output_dir}")

    print("Process analysis completed successfully.")

if __name__ == "__main__":
    main()