# JSON Comparator V1.0

# detect type changement: 
def change_type(old_value, new_value):
    if type(old_value) != type(new_value):
        return True
    return False

# detect value changement:
def change_value(old_value, new_value):
    if old_value != new_value:
        return True
    return False

# detect imbricate field 
def is_imbricate_field(value):
    if isinstance(value, dict):
        return True
    return False

# here we only work on dicts, we don't care about lists for now (we will in V2)
def compare_dicts(old_dict, new_dict, path=""):
    changes = []
    # on traite un champ simple : 
    for key in old_dict:
        # si la clé n'existe pas dans le nouveau dictionnaire , donc supprimée :
        if key not in new_dict:
            changes.append(f"Removed key: {path + key}")
        else : # si la clé exite dans les deux dictionnaires :
            old_value = old_dict[key]
            new_value = new_dict[key]
            # le cas ou c'est le type qui change : 
            if change_type(old_value, new_value):
                changes.append(f"Changed type: {path + key} from {type(old_value).__name__} to {type(new_value).__name__}")
            # le cas ou c'est une imbrication :
            elif is_imbricate_field(old_value) and is_imbricate_field(new_value):
                # si c'est une imbrication , je compare les deux dictionnaires imbriqués en recursivité :
                changes.extend(compare_dicts(old_value, new_value, path + key + "."))
            # le cas ou c'est la valeur qui change :
            elif change_value(old_value, new_value):
                changes.append(f"Changed value: {path + key} from {old_value} to {new_value}")

    for key in new_dict :
        # si la clé n'existe pas dans l'ancien dictionnaire , donc ajoutée :
        if key not in old_dict:
            changes.append(f"Added key: {path + key}")
            new_value = new_dict[key]
            # le cas ou c'est une imbrication :
            if is_imbricate_field(new_value):
                # si c'est une imbrication , je compare les deux dictionnaires imbriqués en recursivité :
                changes.extend(compare_dicts({}, new_value, path + key + "."))

    return changes


# IMPORTANT :
# Si les deux valeurs sont des dictionnaires, change_value sera True
# avant même qu'on teste l'imbrication.
# Donc il faut tester l'imbrication AVANT change_value
# pour pouvoir descendre dans les sous-champs et ne pas perdre le détail.

# CHOIX V1 :
# Quand une clé ajoutée contient un dict,
# on ajoute le parent ET on déplie les champs internes.
#
# POURQUOI :
# Pour voir à la fois qu'un bloc entier est apparu
# ET quels champs précis ont été ajoutés (analyse plus fine).

# NOTE :
# Suppression = parent seulement
# Ajout = parent + champs internes
#
# POURQUOI :
# L'ajout est plus intéressant à analyser (nouvelle donnée créée),
# donc on veut plus de détail que pour la suppression.

# tests
print(compare_dicts({"a": 1}, {"a": 2}))
print(compare_dicts({"a": 1}, {"b": 1}))
print(compare_dicts({"user": {"name": "Ali"}}, {"user": {"name": "Alia"}}))
print(compare_dicts({}, {"user": {"name": "Alia", "age": 30}}))
print( compare_dicts({"a": "1"}, {"a": 1}) )

# output :
# ['Changed value: a from 1 to 2']
# ['Removed key: a', 'Added key: b'] 
# ['Changed value: user.name from Ali to Alia']
# ['Added key: user', 'Added key: user.name', 'Added key: user.age']



