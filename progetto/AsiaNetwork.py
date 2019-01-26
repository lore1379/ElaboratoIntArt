import pysmile
import pysmile_license

class Asia:
    def __init__(self):

# Iniziamo dichiarando la variabile Network. I nodi nel network sono creati
# in sequenza chiamando l'helper method create_cpt_node

        net = pysmile.Network()

        a = self.create_cpt_node(net,
            "asia", "Asia",
            ["Yes","No"],
            60, 40)

        t = self.create_cpt_node(net,
            "tub", "Tuberculosis",
            ["Yes","No"],
            110, 140)

        e = self.create_cpt_node(net,
            "either", "Either",
            ["Yes","No"],
            160, 240)

	x = self.create_cpt_node(net,
            "xray", "XRay",
            ["Yes","No"],
            110, 340)

        l = self.create_cpt_node(net,
            "lung", "LungCancer",
            ["Yes","No"],
            210, 140)

        s = self.create_cpt_node(net,
            "smoke", "Smoke",
            ["Yes","No"],
            260, 40)
        
        b = self.create_cpt_node(net,
            "bronc", "Bronchitis",
            ["Yes","No"],
            260, 140)
        
        d = self.create_cpt_node(net,
            "dysp", "Dyspnea",
            ["Yes","No"],
            260, 240)

#possiamo ora aggiungere gli archi che collegano i nodi

        net.add_arc(a, t);
	net.add_arc(s, l);
	net.add_arc(s, b);
	net.add_arc(l, e);
        net.add_arc(t, e);
	net.add_arc(b, d);
	net.add_arc(e, x);
	net.add_arc(e, d);

	asiaDef = [
            0.01, # P(asia=Y)
            0.99 # P(asia=N)
        ]

# il prossimo step e' la creazione delle tabelle di probabilita' condizionata. Per ogni nodo chiamiamo
# net.set_node_definition e in questo modo settiamo le probabilita'

        net.set_node_definition(a, asiaDef);

        tubDef = [
            0.05, # P(tub=Y|asia=Y)
            0.95, # P(tub=N|asia=Y)
            0.01, # P(tub=Y|asia=N)
            0.99  # P(tub=N|asia=N)
        ]
        net.set_node_definition(t, tubDef);

	smokeDef = [
            0.5, # P(smoke=Y)
            0.5  # P(smoke=N)
        ]
        net.set_node_definition(s, smokeDef);

        lungDef = [
            0.1,  # P(lung=Y|smoke=Y)
            0.9,  # P(lung=N|smoke=Y)
            0.01, # P(lung=Y|smoke=N)
            0.99  # P(lung=N|smoke=N)
        ]
        net.set_node_definition(l, lungDef);

        eitherDef = [
            1, # P(either=Y|lung=Y,tub=Y)
            0, # P(either=N|lung=Y,tub=Y)

            1, # P(either=Y|lung=Y,tub=N)
            0, # P(either=N|lung=Y,tub=N)

            1, # P(either=Y|lung=N,tub=Y)
            0, # P(either=N|lung=N,tub=Y)

            0, # P(either=Y|lung=N,tub=N)
            1  # P(either=N|lung=N,tub=N)
        ]
        net.set_node_definition(e, eitherDef);

	xrayDef = [
            0.98, # P(xray=Y|either=Y)
            0.02, # P(xray=N|either=Y)
            0.05, # P(xray=Y|either=N)
            0.95  # P(xray=N|either=N)
        ]
	net.set_node_definition(x, xrayDef);

        broncDef = [
            0.6,  # P(bronc=Y|smoke=Y)
            0.4,  # P(bronc=N|smoke=Y)
            0.3,  # P(bronc=Y|smoke=N)
            0.7   # P(bronc=N|smoke=N)
        ]
        net.set_node_definition(b, broncDef);

        dyspDef = [
            0.9, # P(dysp=Y|bronc=Y,either=Y)
            0.1, # P(dysp=N|bronc=Y,either=Y)

            0.8, # P(dysp=Y|bronc=Y,either=N)
            0.2, # P(dysp=N|bronc=Y,either=N)

            0.7, # P(dysp=Y|bronc=N,either=Y)
            0.3, # P(dysp=N|bronc=N,either=Y)

            0.1, # P(dysp=Y|bronc=N,either=N)
            0.9  # P(dysp=N|bronc=N,either=N)
        ]
        net.set_node_definition(d, dyspDef);

        print("Network created!")
	print("")

#Update delle probabilita' e si procede a mostrarle usando l'helper method print_all_posteriors

	print("Posteriors with no evidence set:")
        net.update_beliefs()
        self.print_all_posteriors(net)
	print("")
	print("Set or change evidences")
	print("")
        print("Setting Either=Yes, Asia=Yes and Dyspnea=No")
        self.change_evidence_and_update(net, "either", "Yes")
        self.change_evidence_and_update(net, "asia", "Yes")
        self.change_evidence_and_update(net, "dysp", "No")
        print("Setting Smoke=No, changing Either to No, keeping Asia=Yes and Dyspnea=No")
        self.change_evidence_and_update(net, "smoke", "No")
        self.change_evidence_and_update(net, "either", "No")
        print("Removing evidence from Asia and Dyspnea, setting Bronchitis=Yes, keeping Either=No and Smoke=No")
        self.change_evidence_and_update(net, "asia", None)
        self.change_evidence_and_update(net, "dysp", None)
        self.change_evidence_and_update(net, "bronc", "Yes")

        print("Nodes information")
	print("")

        for h in net.get_all_nodes():
            self.print_node_info(net, h)

# La funzione crea un nodo CPT con uno specifico identificatore, nome, risultato e posizione nello
# schermo. I nodi CPT sono creati con due risultati chiamati stato0 e stato1. Per cambiare il numero dei
# risultati e rinominarli usiamo due loops, il primo rinomina i risultati di default e il secondo ne
# ne aggiunge di nuovi.

    def create_cpt_node(self, net, id, name, outcomes, x_pos, y_pos):
        handle = net.add_node(pysmile.NodeType.CPT, id)
        net.set_node_name(handle, name)
        net.set_node_position(handle, x_pos, y_pos, 85, 55)
        initial_outcome_count = net.get_outcome_count(handle)
        for i in range(0, initial_outcome_count):
            net.set_outcome_id(handle, i, outcomes[i])
        for i in range(initial_outcome_count, len(outcomes)):
            net.add_outcome(handle, outcomes[i])
        return handle

# print_posteriors controlla se il nodo ha evidenza chiamando net.is_evidence;
# in caso positivo il nome dell' evidenza viene mostrato.
# print_posteriors itera su tutti gli stati e mostra la posterior probability di ognuno.
# cambiamo ripetutamente change_evidence_and_update per cambiare le evidenze,
# aggiornare il network e mostrare i posteriors.

    def print_posteriors(self, net, node_handle):
        node_id = net.get_node_id(node_handle)
        if net.is_evidence(node_handle):
            print(node_id + " has evidence set (" +
                  net.get_outcome_id(node_handle, 
                                     net.get_evidence(node_handle)) + ")")
        else :
            posteriors = net.get_node_value(node_handle)
            for i in range(0, len(posteriors)):
                print("P(" + node_id + "=" + 
                      net.get_outcome_id(node_handle, i) +
                      ")=" + str(posteriors[i]))

# print_all_posteriors mostra le posterior probabilities calcolate da update_beliefs per ogni nodo.
# Per iterare sui nodi sono usati net.get_first_node e get_next_node.

    def print_all_posteriors(self, net):
        handles = net.get_all_nodes()
        for h in handles:
            self.print_posteriors(net, h)
    
    def change_evidence_and_update(self, net, node_id, outcome_id):
        if outcome_id is not None:
            net.set_evidence(node_id, outcome_id)	
        else:
            net.clear_evidence(node_id)
        
        net.update_beliefs()
        self.print_all_posteriors(net)
        print("")

    def print_node_info(self, net, node_handle):

# Per prima cosa mostriamo indentificatore e il nome del nodo.

        print("Node id/name: " + net.get_node_id(node_handle) + "/" +
              net.get_node_name(node_handle))

# Ora i risultati del nodo.

        print(" Outcomes: " + " ".join(net.get_outcome_ids(node_handle)))
        parent_ids = net.get_parent_ids(node_handle)

# i nodi genitori.

        if len(parent_ids) > 0:
            print(" Parents: " + " ".join(parent_ids))
        child_ids = net.get_child_ids(node_handle)

# i nodi figli. parents_ids e child_ids restituisce gli indentificatori

        if len(child_ids) > 0:
            print(" Children: " + " ".join(child_ids))
        self.print_cpt_matrix(net, node_handle)

# le probabilita' dei nodi sono mostrate da print_cpt_matrix. Dall'array prendiamo le probabilita'
# con get_node_definition e li traduciamo in un array multidimensionale (grazie al metodo index_to_coords)

    def print_cpt_matrix(self, net, node_handle):
        cpt = net.get_node_definition(node_handle)
        parents = net.get_parents(node_handle)
        dim_count = 1 + len(parents)

        dim_sizes = [0] * dim_count
        for i in range(0, dim_count - 1):
            dim_sizes[i] = net.get_outcome_count(parents[i])
        dim_sizes[len(dim_sizes) - 1] = net.get_outcome_count(node_handle)

        coords = [0] * dim_count
        for elem_idx in range(0, len(cpt)):
            self.index_to_coords(elem_idx, dim_sizes, coords)
            outcome = net.get_outcome_id(node_handle, coords[dim_count - 1])
            out_str = " P(" + outcome
            if dim_count > 1:
                out_str += " | "
                for parent_idx in range(0, len(parents)):
                    if parent_idx > 0:
                        out_str += ","
                    parent_handle = parents[parent_idx]
                    out_str += net.get_node_id(parent_handle) + "=" + \
                    net.get_outcome_id(parent_handle, coords[parent_idx])
            prob = cpt[elem_idx]
            out_str += ")=" + str(prob)
            print(out_str)

    def index_to_coords(self, index, dim_sizes, coords):
        prod = 1
        for i in range(len(dim_sizes) - 1, -1, -1):
            coords[i] = (index / prod) % dim_sizes[i]
            prod *= dim_sizes[i]