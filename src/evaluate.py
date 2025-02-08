import subprocess

def evaluate_results(results_file="../results/Results.txt", qrels_file="../data/scifact/test.tsv"):
    command = f"./trec_eval {qrels_file} {results_file}"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    print(output.decode())

if __name__ == "__main__":
    evaluate_results()