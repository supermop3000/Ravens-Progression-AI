# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
from PIL import ImageChops
import numpy
import math
import operator
import functools
from pprint import pprint as pp
from decimal import Decimal

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        print('testing')

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        prob_type = ''
        transform_check = 0
        transform_type = ''

        print(problem.name)
        print(problem.problemType)

        if(problem.problemType == "2x2"):
            prob_type = 'four'
        elif(problem.problemType == "3x3"):
            prob_type = 'nine'
            answer = 0

        if(prob_type == 'four'):
            transform_check = 2

        elif (prob_type == 'nine'):
            transform_check = 3

        if transform_check == 2:
            all_trans = self.getAllTransforms(problem)
            answer = self.getHeroTransform(all_trans)

        return answer

    def getAllTransforms(self, problem):
        all_trans = {}

        for x in range (1,7):
            a_id = 'A' + str(x)
            b_id = 'B' + str(x)
            c_id = 'C' + str(x)
            all_trans[a_id] = self.getTransform(a_id, Image.open(problem.figures['A'].visualFilename), Image.open(problem.figures[str(x)].visualFilename))
            all_trans[b_id] = self.getTransform(b_id, Image.open(problem.figures['B'].visualFilename), Image.open(problem.figures[str(x)].visualFilename))
            all_trans[c_id] = self.getTransform(c_id, Image.open(problem.figures['C'].visualFilename), Image.open(problem.figures[str(x)].visualFilename))

        all_trans['AB'] = self.getTransform('AB', Image.open(problem.figures['A'].visualFilename), Image.open(problem.figures['B'].visualFilename))
        all_trans['AC'] = self.getTransform('AC', Image.open(problem.figures['A'].visualFilename), Image.open(problem.figures['C'].visualFilename))
        all_trans['BC'] = self.getTransform('BC', Image.open(problem.figures['B'].visualFilename), Image.open(problem.figures['C'].visualFilename))

        pp(all_trans)

        return all_trans

    def checkSame(self, img_a, img_b):
        a1 = numpy.array(img_a)
        a2 = numpy.array(img_b)

        a1[a1 >= 128] = 255
        a2[a2 < 128] = 0

        num_equal_elements = numpy.sum(a1 == a2)
        total_elements = numpy.count_nonzero(a1 >= 0)
        percent = (num_equal_elements / total_elements)*2

        return percent

    def checkMirrorHoriz(self, image_a, image_b):
        img_a_h_mirror = image_a.transpose(Image.FLIP_LEFT_RIGHT)
        return self.checkSame(img_a_h_mirror, image_b)

    def checkMirrorVert(self, image_a, image_b):
        img_a_v_mirror = image_a.transpose(Image.FLIP_TOP_BOTTOM)
        return self.checkSame(img_a_v_mirror, image_b)

    def checkRotate90(self, image_a, image_b):
        ninety = image_a.transpose(Image.ROTATE_90)
        return self.checkSame(ninety, image_b)

    def checkRotate270(self, image_a, image_b):
        twoseventy = image_a.transpose(Image.ROTATE_270)
        return self.checkSame(twoseventy, image_b)

    #TODO: This function sucks! Need to rewrite
    def checkDelete(self, image_a, image_b):
        image_diff = ImageChops.difference(image_a, image_b)
        inv_image_diff = ImageChops.invert(image_diff)
        composite = ImageChops.multiply(image_b, inv_image_diff)

        if self.checkSame(image_a, composite) == 1.0:
            return 0
        else:
            return self.checkSame(image_a, composite)

    #TODO: This function sucks! Need to rewrite, also write a difference function?
    def checkAdd(self, image_a, image_b):
        image_diff = ImageChops.difference(image_a, image_b)
        inv_image_diff = ImageChops.invert(image_diff)
        composite = ImageChops.multiply(image_a, inv_image_diff)

        return self.checkSame(image_b, composite)

    def getTransform(self, id, image_a, image_b):

        transform = {}

        transform['same'] = {'val': self.checkSame(image_a, image_b), 'id': id}
        transform['mirror_horiz'] = {'val': self.checkMirrorHoriz(image_a, image_b), 'id': id}
        transform['mirror_vert'] = {'val': self.checkMirrorVert(image_a, image_b), 'id': id}
        transform['rotate_90'] = {'val': self.checkRotate90(image_a, image_b)-.1,  'id': id}
        transform['rotate_270'] = {'val': self.checkRotate270(image_a, image_b)-.1, 'id': id}
        transform['delete'] = {'val': self.checkDelete(image_a, image_b)-.1,  'id': id}
        transform['add'] = {'val': self.checkAdd(image_a, image_b)-.1, 'id': id}

        return transform

    def getHeroTransform(self, all_trans):
        hero_dict_ab = {}
        hero_dict_ac = {}
        hero_dict_bc = {}

        print(all_trans['AB'])
        print('- - - - - - - - - - - -  --  - - - - - -- - - - - - - - - - - - - - - -  -- - - - -- -  --')
        print(all_trans['C1'])

        for key in all_trans['AB']:
            for x in range(1, 7):
                for subkey in all_trans['C' + str(x)]:
                    if key == subkey:
                        print(subkey)
                        hero_val_a = all_trans['C' + str(x)].get(key).get('val') + (all_trans['AB'].get(key).get('val'))
                        hero_dict_ab['C' + str(x), subkey] = hero_val_a

        for key in all_trans['AC']:
            for x in range(1, 7):
                for subkey in all_trans['B' + str(x)]:
                    if key == subkey:
                        hero_val_b = all_trans['B' + str(x)].get(key).get('val') + (all_trans['AC'].get(key).get('val'))
                        hero_dict_ac['B' + str(x), subkey] = hero_val_b

        for key in all_trans['BC']:
            for x in range(1,7):
                for subkey in all_trans['A' + str(x)]:
                    if key == subkey:
                        hero_val_c = all_trans['A' + str(x)].get(key).get('val') + (all_trans['BC'].get(key).get('val'))
                        hero_dict_bc['A' + str(x), subkey] = hero_val_c

        pp(hero_dict_ab)
        pp(hero_dict_ac)
        pp(hero_dict_bc)

        ab_max_key = max(hero_dict_ab, key=hero_dict_ab.get)
        ab_max_val = hero_dict_ab.get(ab_max_key)
        ac_max_key = max(hero_dict_ac, key=hero_dict_ac.get)
        ac_max_val = hero_dict_ac.get(ac_max_key)
        bc_max_key = max(hero_dict_bc, key=hero_dict_bc.get)
        bc_max_val = hero_dict_bc.get(bc_max_key)

        print(hero_dict_ab)
        print('AB HIGH: ' + str(ab_max_key) + ': ' + str(hero_dict_ab.get(ab_max_key)))
        print(hero_dict_ac)
        print('AC HIGH: ' + str(ac_max_key) + ': ' + str(hero_dict_ac.get(ac_max_key)))
        print(hero_dict_bc)
        print('BC HIGH: ' + str(bc_max_key) + ': ' + str(hero_dict_bc.get(bc_max_key)))

        if ab_max_val >= ac_max_val and ab_max_val >= bc_max_val:
            ans = ab_max_key

        elif ac_max_val > ab_max_val and ac_max_val >= bc_max_val:
            ans = ac_max_key

        elif bc_max_val > ab_max_val and bc_max_val > ac_max_val:
            ans = bc_max_key

        answer_str = str(ans[0])
        answer = int(answer_str[1])

        print(answer)

        return answer

