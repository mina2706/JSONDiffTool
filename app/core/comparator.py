# JSON Comparator V1.0

####################################################### UTILS ####################################################################################
#================================================================================================================================================#
##################################################################################################################################################
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


####################################################### DICTS ####################################################################################
#================================================================================================================================================#
##################################################################################################################################################

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
            elif isinstance(old_value, dict) and isinstance(new_value, dict): 
                # si c'est une imbrication , je compare les deux dictionnaires imbriqués en recursivité :
                changes.extend(compare_dicts(old_value, new_value, path + key + "."))
            elif isinstance(old_value, list) and isinstance(new_value, list):
                # si c'est une imbrication , je compare les deux listes imbriquées en recursivité :
                print("j'étais là .........................aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                changes.extend(compare_lists(old_value, new_value, path + key)) # là pas de point pour séparer le parent du champ interne, car c'est une liste, pas un dict
            # le cas ou c'est la valeur qui change :
            elif change_value(old_value, new_value):
                changes.append(f"Changed value: {path + key} from {old_value} to {new_value}")

    for key in new_dict :
        # si la clé n'existe pas dans l'ancien dictionnaire , donc ajoutée :
        if key not in old_dict:
            changes.append(f"Added key: {path + key}")
            new_value = new_dict[key]
            # le cas ou c'est une imbrication :
            if isinstance(new_value, dict):
                # si c'est une imbrication , je compare les deux dictionnaires imbriqués en recursivité :
                changes.extend(compare_dicts({}, new_value, path + key + "."))
            elif isinstance(new_value, list):
                # si c'est une imbrication , je compare les deux listes imbriquées en recursivité :
                changes.extend(compare_lists([], new_value, path + key)) # là pas de point pour séparer le parent du champ interne, car c'est une liste, pas un dict

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

####################################################### LISTS ####################################################################################
#================================================================================================================================================#
##################################################################################################################################################

def compare_lists( old_list, new_list, path=""):
    changes = []
    for i in range (max(len(old_list), len(new_list))):
        # le cas où y a un élément à cette position dans les 2 listes: 
        if i<len(old_list) and i<len(new_list):
            old_value = old_list[i]
            new_value = new_list[i]
            # changement de type : 
            if change_type(old_value, new_value):
                changes.append(f"Changed type: {path}[{i}] from {type(old_value).__name__} to {type(new_value).__name__}")
            # imbrication :
            elif isinstance(old_value, dict) and isinstance(new_value, dict): # cas de dict imbriqué
                changes.extend(compare_dicts(old_value, new_value, path + f"[{i}]."))
            elif isinstance(old_value, list) and isinstance(new_value, list): # cas de liste imbriquée
                changes.extend(compare_lists(old_value, new_value, path + f"[{i}]."))
            # changement de valeur :
            elif change_value(old_value, new_value):
                changes.append(f"Changed value: {path}[{i}] from {old_value} to {new_value}")
        # le cas où y a un élément à cette position que dans l'ancienne liste :
        # ça reste pas précis : on sait juste qu'un élément a été supprimé à cette position, mais pas s'il s'agit d'un élément supprimé ou d'un déplacement d'élément existant.
        elif i<len(old_list) and i>=len(new_list):
            changes.append(f"Removed element: {path}[{i}] with value {old_list[i]}")
        # le cas où y a un élément à cette position que dans la nouvelle liste :
        # ça reste pas précis : on sait juste qu'un élément a été ajouté à cette position, mais pas s'il s'agit d'un nouvel élément ou d'un déplacement d'élément existant.
        elif i>=len(old_list) and i<len(new_list): 
            changes.append(f"Added element: {path}[{i}] with value {new_list[i]}")
        
    return changes

# NOTE :
# cette approche n'est pas la plus optimale pour comparer des listes, car elle est très sensible aux changements d'ordre et aux ajouts/suppressions d'éléments.
# Par exemple, si on ajoute un élément au début d'une liste, tous les éléments suivants seront considérés comme "changement de valeur" alors qu'en réalité il s'agit juste d'un décalage.
# Dans un cadre métier ... y aura certainement des pertes de précision dans les changements détectés, mais ça peut être suffisant pour une première version.


# tests
print(compare_dicts({"a": 1}, {"a": 2})) # ['Changed value: a from 1 to 2']
print(compare_dicts({"a": 1}, {"b": 1})) # ['Removed key: a', 'Added key: b'] 
print(compare_dicts({"user": {"name": "Ali"}}, {"user": {"name": "Alia"}})) # ['Changed value: user.name from Ali to Alia']
print(compare_dicts({}, {"user": {"name": "Alia", "age": 30}})) # ['Added key: user', 'Added key: user.name', 'Added key: user.age']
print( compare_dicts({"a": "1"}, {"a": 1}) ) # ['Changed type: a from str to int']
print( compare_dicts({"a": [1, 2]}, {"a": [1, 3]}) ) # ['Changed value: a from [1, 2] to [1, 3]']
print( compare_dicts({"a": [1, 2]}, {"a": [1, 3]}) ) # ['Changed value: a from [1, 2] to [1, 3]'] 


# tests
print ("============================================ TESTS LISTS ============================================")
print(compare_lists([1, 2, 3], [1, 4, 3])) 
print(compare_lists([1, 2, 3], [1, 2, 3, 4])) 
print(compare_lists([1, 2, 3], [0, 1, 2, 3])) 
#print(compare_lists([1, 2, 3], [2, 3])) # ['Changed value: [0] from 1 to 2', 'Changed value: [1] from 2 to 3', 'Changed value: [2] from 3 to None'] 
# c'est bizarre mais on le garde pour le en cas de suppression d'élément au début de la liste (décalage de tous les éléments suivants)
print(compare_lists([{"a": 1}, {"b": 2}], [{"a": 1}, {"b": 3}])) # ['Changed value: [1].b from 2 to 3']
print(compare_lists([{"a": [1, 2]}], [{"a": [1, 3]}])) #( je suppose que ça ne va pas passé parceque compare_dicts ne gère pas les listes imbriquées, 
# mais c'est pour illustrer l'idée, maintenant ça marche ;))
print(compare_lists([1,[2, 3]], [1,[2, 4]])) #( ça passera normalement parceque compare_lists gère les listes imbriquées)

# output :
# ['Changed value: [1] from 2 to 4']
# ['Added element: [3] with value 4']
# ['Changed value: [0] from 1 to 0', 'Changed value: [1] from 2 to 1', 'Changed value: [2] from 3 to 2', 'Added element: [3] with value 3']
# ['Changed value: [1].b from 2 to 3']
# ['Changed value: [0].a.[1] from 2 to 3'] // là il y a un probléme de formatage du path, il faudrait que ça soit [0].a[1] au lieu de [0].a.[1] c'est fixé ( regarde la li)
# ['Changed value: [1].[1] from 3 to 4'] 

# TODO
# test unitaire pour compare_lists
# comapre list est bien utilisé dans compare dict qd on l'appelle dans comapre_list .. mais pas qd on appelle compare dict directemnt ... je comprends à peine pourquoi ... à vérifier
# amélioration de la précision des changements détectés dans les listes (ex: détection de déplacement d'éléments, plutôt que juste ajout/suppression)
# fixer le probléme de l'utilsation de compare_lists dans compare_dict