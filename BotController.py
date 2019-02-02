import popo.AccountGroup as AG
import popo.Account as A
import random
import popo.RallyGroup as RG
import util.MapNavigator as MN
import subprocess



def gather_rss(rss_name):
    mode = 1
    MN.open_map()
    MN.nav_map(mode)
    

#INCOMPLETE (we should make sure there's a pause button somewhere)

#INCOMPLETE
def rally_group_to_action(rg) -> function:
    def action():
        print('yes')
    return action

#both account actions will be linked
def generate_linked_action(actionlist, a1, a2) -> function:
    def linked_action():
        return
    return linked_action

def rally_group_check(rg, account) -> None:
    if(account == None):
        return
    farmtype = account.farmtype
    if (farmtype == 2):
        rg.add_follower(account)
    elif (farmtype == 3):
        rg.add_leader(account)



def generate_actionlist(farmgroups) -> [function]:
    actionlist = []
    rg = RG.RallyGroup()
    for fg in farmgroups:
        account1 = fg.account1
        account2 = fg.account2
        rally_group_check(rg,account1)
        rally_group_check(rg,account2)
        generate_linked_action(actionlist, account1, account2)
        actionlist.append(rally_group_to_action(rg))





def main() -> int:
    farmgroups = [AG.AccountGroup(A.Account('OFFENS2', 2), A.Account('OFFENS3', 2), scrolllocation=),
                  AG.AccountGroup(A.Account('OFFENS4', 3), None, scrolllocation=),
                  AG.AccountGroup(A.Account('OFFENS5', 2), A.Account('OFFENS6', 2), scrolllocation=),
                  AG.AccountGroup(A.Account('OFFENS7', 1), A.Account('OFFENS8', 1), scrolllocation=),
                  AG.AccountGroup(A.Account('OFFENS9', 1), A.Account('OFFENS10', 1), scrolllocation=),
                  AG.AccountGroup(A.Account('WOLFKING0', 1), A.Account('WOLFKING1', 1), scrolllocation=),
                  AG.AccountGroup(A.Account('WOLFKING2', 1), None, scrolllocation=),
                  AG.AccountGroup(A.Account('WOLFKING3', 1), A.Account('WOLFKING4', 1), scrolllocation=),
                  AG.AccountGroup(A.Account('WOLFKING5', 1), None, scrolllocation=)]
    actionlist = generate_actionlist(farmgroups)
    random.shuffle(actionlist)
    map(eval,actionlist)


    return 0



if __name__=='__main__':
    main()