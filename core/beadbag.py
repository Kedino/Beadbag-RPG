import random 

class Beadbag():
    def __init__(self):
        self.beads_in_bag = []

    def add_bead(self, color, permanence):
        bead = {'color': color, 'permanence': permanence}
        self.beads_in_bag.append(bead)

    def remove_bead(self, bead):
        if bead in self.beads_in_bag:
            self.beads_in_bag.remove(bead)

    def list_beads(self):
        return self.beads_in_bag
    
    def should_be_removed(self, bead, clear_persist=False):
        if bead['permanence'] == 'temporary':
            return True
        elif bead['permanence'] == 'persistent' and clear_persist:
            return True
        return False        
        
    #def draw_bead(self, amount=5):        
    #    if len(self.beads_in_bag) < amount:
    #        raise ValueError("Not enough beads in the bag to draw.")
    #    drawn = random.sample(self.beads_in_bag, amount)
    #    for bead in drawn:
    #        self.beads_in_bag.remove(bead)
    #    self.drawn_beads.extend(drawn)
    #    return self.drawn_beads
    
    #def return_drawn_beads(self):
    #    self.beads_in_bag.extend(self.drawn_beads)
    #    self.drawn_beads.clear()

    #def cleanup_bag(self, clear_persist=False):
    #    new_bag_content = []
    #    for bead in self.beads_in_bag:            
    #        if bead["permanence"] == 'permanent':
    #            new_bag_content.append(bead)
    #        elif bead["permanence"] == 'persistent' and not clear_persist:
    #            new_bag_content.append(bead)
    #        else:
    #            continue
    #    self.beads_in_bag = new_bag_content



class Drawbag(Beadbag):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def draw_bead(self, amount=5):
        if len(self.parent.beads_in_bag) < amount:
            raise ValueError("Not enough beads in the bag to draw.")
        drawn = random.sample(self.parent.beads_in_bag, amount)
        for bead in drawn:
            self.parent.remove_bead(bead)
            self.beads_in_bag.append(bead)
        return self.beads_in_bag

    def return_bead(self, bead):
        if bead in self.beads_in_bag:
            self.beads_in_bag.remove(bead)
            self.parent.add_bead(bead['color'], bead['permanence'])
        
    def redraw_bead(self, bead):
        if bead in self.beads_in_bag:
            self.return_bead(bead)
            return self.draw_bead(amount=1)
        
    def resolve_draw(self, clear_persist=False):
        for bead in self.beads_in_bag[:]:
            if self.should_be_removed(bead, clear_persist):
                self.remove_bead(bead)
            else:
                self.parent.add_bead(bead['color'], bead['permanence'])
                self.remove_bead(bead)