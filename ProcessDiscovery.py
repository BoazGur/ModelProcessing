import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.alpha import algorithm as alpha_miner
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner
from pm4py.visualization.petri_net import visualizer as pn_visualizer
from pm4py.visualization.transition_system import visualizer as ts_visualizer
from pm4py.visualization.graphs import visualizer as graphs_visualizer
from pm4py.algo.discovery.transition_system import algorithm as ts_discovery
from pm4py.objects.petri_net.utils import reachability_graph
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness
from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.generalization import algorithm as generalization_evaluator
from pm4py.algo.evaluation.simplicity import algorithm as simplicity_evaluator
import matplotlib.pyplot as plt

class ProcessDiscovery:
    def __init__(self):
        self.log = None
        self.net = None
        self.initial_marking = None
        self.final_marking = None

    def import_log(self, xes_file):
        self.log = xes_importer.apply(xes_file)
        print(f"Log imported successfully from {xes_file}")

    def discover_process(self, algorithm='alpha'):
        if self.log is None:
            raise ValueError("Log not imported. Use import_log() method first.")

        if algorithm == 'alpha':
            self.net, self.initial_marking, self.final_marking = alpha_miner.apply(self.log)
        elif algorithm == 'inductive':
            self.net, self.initial_marking, self.final_marking = inductive_miner.apply(self.log)
        elif algorithm == 'heuristics':
            self.net, self.initial_marking, self.final_marking = heuristics_miner.apply(self.log)
        else:
            raise ValueError("Unsupported algorithm. Choose 'alpha', 'inductive', or 'heuristics'.")
        
        print(f"Process model discovered using {algorithm} miner.")

    def perform_conformance_checking(self):
        if self.net is None:
            raise ValueError("Process model not discovered. Use discover_process() method first.")

        fitness = replay_fitness.apply(self.log, self.net, self.initial_marking, self.final_marking)
        precision = precision_evaluator.apply(self.log, self.net, self.initial_marking, self.final_marking)
        generalization = generalization_evaluator.apply(self.log, self.net, self.initial_marking, self.final_marking)
        simplicity = simplicity_evaluator.apply(self.net)

        results = {
            'fitness': fitness['log_fitness'],
            'precision': precision,
            'generalization': generalization,
            'simplicity': simplicity
        }

        print("Conformance checking completed.")
        return results

    def plot_petri_net(self, file_path="petri_net.png"):
        if self.net is None:
            raise ValueError("Process model not discovered. Use discover_process() method first.")

        gviz = pn_visualizer.apply(self.net, self.initial_marking, self.final_marking)
        pn_visualizer.save(gviz, file_path)
        print(f"Petri net visualization saved to {file_path}")

    def plot_reachability_graph(self, file_path="reachability_graph.png"):
        if self.net is None:
            raise ValueError("Process model not discovered. Use discover_process() method first.")

        reach_graph = reachability_graph.construct_reachability_graph(self.net, self.initial_marking)
        gviz = graphs_visualizer.apply(reach_graph, parameters={graphs_visualizer.Variants.NETWORKX.value.Parameters.FORMAT: "png"})
        graphs_visualizer.save(gviz, file_path)
        print(f"Reachability graph visualization saved to {file_path}")

    def plot_transition_system(self, file_path="transition_system.png"):
        if self.log is None:
            raise ValueError("Log not imported. Use import_log() method first.")

        ts = ts_discovery.apply(self.log)
        gviz = ts_visualizer.apply(ts, parameters={ts_visualizer.Variants.VIEW_BASED.value.Parameters.FORMAT: "png"})
        ts_visualizer.save(gviz, file_path)
        print(f"Transition system visualization saved to {file_path}")

    def visualize_markings(self, file_path="markings.png"):
        if self.net is None:
            raise ValueError("Process model not discovered. Use discover_process() method first.")

        gviz = pn_visualizer.apply(self.net, self.initial_marking, self.final_marking)
        
        for place in gviz.node_attr:
            if place in self.initial_marking:
                gviz.node_attr[place]['color'] = 'green'
                gviz.node_attr[place]['style'] = 'filled'
                gviz.node_attr[place]['fillcolor'] = 'lightgreen'
            elif place in self.final_marking:
                gviz.node_attr[place]['color'] = 'red'
                gviz.node_attr[place]['style'] = 'filled'
                gviz.node_attr[place]['fillcolor'] = 'lightpink'
        
        pn_visualizer.save(gviz, file_path)
        print(f"Petri net with marked initial and final places saved to {file_path}")
        
        print("\nExplanation of Markings:")
        print("- Initial Marking (Green):")
        for place in self.initial_marking:
            print(f"  - Place: {place.name}, Tokens: {self.initial_marking[place]}")
        print("  This represents the starting state of the process.")
        
        print("\n- Final Marking (Red):")
        for place in self.final_marking:
            print(f"  - Place: {place.name}, Tokens: {self.final_marking[place]}")
        print("  This represents the desired end state(s) of the process.")

    def visualize_conformance(self, conformance_results, file_path="conformance_metrics.png"):

        metrics = ['Fitness', 'Precision', 'Generalization', 'Simplicity']
        values = [conformance_results['fitness'], conformance_results['precision'], 
                  conformance_results['generalization'], conformance_results['simplicity']]
        
        plt.figure(figsize=(10, 6))
        plt.bar(metrics, values)
        plt.title('Conformance Checking Metrics')
        plt.ylabel('Score')
        plt.ylim(0, 1)
        for i, v in enumerate(values):
            plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')
        plt.savefig(file_path)
        plt.close()
        print(f"Conformance metrics visualization saved to {file_path}")

    def run_full_analysis(self, xes_file, output_dir="process_analysis_output", algorithm='inductive'):
        os.makedirs(output_dir, exist_ok=True)

        self.import_log(xes_file)
        self.discover_process(algorithm)

        self.plot_petri_net(os.path.join(output_dir, "petri_net.png"))
        self.plot_reachability_graph(os.path.join(output_dir, "reachability_graph.png"))
        self.plot_transition_system(os.path.join(output_dir, "transition_system.png"))
        self.visualize_markings(os.path.join(output_dir, "markings.png"))

        conformance_results = self.perform_conformance_checking()
        self.visualize_conformance(conformance_results, os.path.join(output_dir, "conformance_metrics.png"))

        print(f"Full analysis completed. All visualizations saved in {output_dir}")