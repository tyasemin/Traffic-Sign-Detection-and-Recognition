import os

#get labels and paths
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

file=open(os.path.join(__location__,"all_path.txt"))
all_path=file.readlines()
file.close()

total_num=len(all_path)
train_num=int(total_num*75/100)
val_num=int(total_num*20/100)
test_num=total_num-train_num-val_num

train_file=open(os.path.join(__location__,"train.txt"),"w")
for i in range(train_num):
    train_file.write(all_path[i])
train_file.close()

val_file=open(os.path.join(__location__,"val.txt"),"w")
for i in range(train_num,(train_num+val_num)):
    val_file.write(all_path[i])
val_file.close()

test_file=open(os.path.join(__location__,"test.txt"),"w")
for i in range((train_num+val_num),total_num):
    test_file.write(all_path[i])
test_file.close()

















            







     
    
    
    


    


file.close()




