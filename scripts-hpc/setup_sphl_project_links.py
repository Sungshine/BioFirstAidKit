#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" Setup state-user organism projects and sym-links

    Script should be run as user: 'ce'

"""


import os



def make_refid(state):
    """ RefId Projects

        Should contain the following sym-links:
        # BACT -> /data/shared/searchdata_wgmlst_adb_refid_v1/BACT
        # contamination -> /data/shared/Contamination/midas_db_v1.2
        # speciation -> /data/ceroot/bin/ani/references_v2

    """

    shared_dir = '/data/shared'
    ceroot_dir = '/data/ceroot'
    labid = state
    ref_dir = '{}_refid'.format(labid)

    dir_path = os.path.join(shared_dir, ref_dir)

    if not os.path.isdir(dir_path):
        # To be safe, we will not create new directories
        # print('Creating directory: {}'.format(dir_path))
        print('{} does not exist'.format(dir_path))
        os.mkdir(dir_path)
    else:
        print('{} already exists!'.format(os.path.basename(dir_path)))

        # Link sources
        src_ani = os.path.join(ceroot_dir, 'bin/ani/references_v2')
        src_alleles = os.path.join(shared_dir, 'searchdata_wgmlst_adb_refid_v1/BACT')
        src_midas = os.path.join(shared_dir, 'Contamination/midas_db_v1.2')
        assert os.path.isdir(src_ani), 'Unable to find: {}'.format(src_ani)
        assert os.path.isdir(src_alleles), 'Unable to find: {}'.format(src_alleles)
        assert os.path.isdir(src_midas), 'Unable to find: {}'.format(src_midas)
        # Link destinations
        alleles_dst = os.path.join(dir_path, 'BACT')
        ani_dst = os.path.join(dir_path, 'speciation')
        midas_dst = os.path.join(dir_path, 'contamination')

        links_to_check = {
            alleles_dst: src_alleles,
            ani_dst: src_ani,
            midas_dst: src_midas,
            }

        for dst, src in links_to_check.iteritems():
            if os.path.islink(dst):
                print('{} --> {} already exists!'.format(src, dst))
            else:
                try:
                    os.symlink(src, dst)
                    print('Success linking {} --> {}'.format(os.path.basename(dst), src))
                except Exception as e:
                    print('Error linking {} --> {}'.format(os.path.basename(dst), src))
                    print(e)

            assert os.path.islink(dst), '{} is missing link: {}'.format(os.path.basename(dir_path), os.path.basename(dst))


def make_salm(state):
    """ Salmonella Projects

        Should contain the following sym-links:
        # ani_references -> /data/shared/ANI/CDC_EDLB_salmonella
        # SALM -> /data/shared/searchdata_wgmlst_adb_salm_v3/SALM
        # speciation -> /data/shared/ANI/CDC_EDLB_salmonella

    """

    shared_dir = '/data/shared'
    labid = state
    salm_dir = '{}_salmonella'.format(labid)

    dir_path = os.path.join(shared_dir, salm_dir)

    if not os.path.isdir(dir_path):
        # To be safe, we will not create new directories
        # print('Creating directory: {}'.format(dir_path))
        print('{} does not exist'.format(dir_path))
        # os.mkdir(dir_path)
    else:
        print('{} already exists!'.format(os.path.basename(dir_path)))

        # Link sources
        src_ani = os.path.join(shared_dir, 'ANI/CDC_EDLB_salmonella')
        src_alleles = os.path.join(shared_dir, 'searchdata_wgmlst_adb_salm_v3/SALM')
        assert os.path.isdir(src_ani), 'Unable to find: {}'.format(src_ani)
        assert os.path.isdir(src_alleles), 'Unable to find: {}'.format(src_alleles)
        # Link destinations
        refid_dst = os.path.join(dir_path, 'ani_references')
        alleles_dst = os.path.join(dir_path, 'SALM')
        ani_dst = os.path.join(dir_path, 'speciation')

        links_to_check = {
            refid_dst: src_ani,
            ani_dst: src_ani,
            alleles_dst: src_alleles,
            }

        for dst, src in links_to_check.iteritems():
            if os.path.islink(dst):
                print('{} --> {} already exists!'.format(src, dst))
            else:
                try:
                    os.symlink(src, dst)
                    print('Success linking {} --> {}'.format(os.path.basename(dst), src))
                except Exception as e:
                    print('Error linking {} --> {}'.format(os.path.basename(dst), src))
                    print(e)

            assert os.path.islink(dst), '{} is missing link: {}'.format(os.path.basename(dir_path), os.path.basename(dst))


def make_lmo(state):
    """ Listeria Projects

        Should contain the following sym-links:
        ani_references -> /data/shared/ANI/CDC_EDLB_listeria
        LMO -> /data/shared/searchdata_wgmlst_adb_lmo_v5/LMO
        speciation -> /data/shared/ANI/CDC_EDLB_listeria

    """

    shared_dir = '/data/shared'
    labid = state
    lmo_dir = '{}_listeria'.format(labid)

    dir_path = os.path.join(shared_dir, lmo_dir)

    if not os.path.isdir(dir_path):
        # To be safe, we will not create new directories
        # print('{} does not exist'.format(dir_path))
        print('Creating directory: {}'.format(dir_path))
        os.mkdir(dir_path)
    else:
        print('{} already exists!'.format(os.path.basename(dir_path)))

        # Link sources
        src_ani = os.path.join(shared_dir, 'ANI/CDC_EDLB_listeria')
        src_alleles = os.path.join(shared_dir, 'searchdata_wgmlst_adb_lmo_v5/LMO')
        assert os.path.isdir(src_ani), 'Unable to find: {}'.format(src_ani)
        assert os.path.isdir(src_alleles), 'Unable to find: {}'.format(src_alleles)
        # Link destinations
        refid_dst = os.path.join(dir_path, 'ani_references')
        alleles_dst = os.path.join(dir_path, 'LMO')
        ani_dst = os.path.join(dir_path, 'speciation')

        links_to_check = {
            refid_dst: src_ani,
            ani_dst: src_ani,
            alleles_dst: src_alleles,
            }

        for dst, src in links_to_check.iteritems():
            if os.path.islink(dst):
                print('{} --> {} already exists!'.format(src, dst))
            else:
                try:
                    os.symlink(src, dst)
                    print('Success linking {} --> {}'.format(os.path.basename(dst), src))
                except Exception as e:
                    print('Error linking {} --> {}'.format(os.path.basename(dst), src))
                    print(e)

            assert os.path.islink(dst), '{} is missing link: {}'.format(os.path.basename(dir_path), os.path.basename(dst))


def make_ecoli(state):
    """ Escherichia Projects

        Should contain the following sym-links:
        EC -> /data/shared/searchdata_wgmlst_adb_cdc_ecoli_v4/EC

    """

    shared_dir = '/data/shared'
    labid = state
    ec_dir = '{}_escherichia'.format(labid)

    dir_path = os.path.join(shared_dir, ec_dir)

    if not os.path.isdir(dir_path):
        # To be safe, we will not create new directories
        # print('{} does not exist'.format(dir_path))
        print('Creating directory: {}'.format(dir_path))
        os.mkdir(dir_path)
    else:
        print('{} already exists!'.format(os.path.basename(dir_path)))

        # Link sources
        src_alleles = os.path.join(shared_dir, 'searchdata_wgmlst_adb_cdc_ecoli_v4/EC')
        assert os.path.isdir(src_alleles), 'Unable to find: {}'.format(src_alleles)
        # Link destinations
        alleles_dst = os.path.join(dir_path, 'EC')

        links_to_check = { alleles_dst: src_alleles }

        for dst, src in links_to_check.iteritems():
            if os.path.islink(dst):
                print('{} --> {} already exists!'.format(src, dst))
            else:
                try:
                    os.symlink(src, dst)
                    print('Success linking {} --> {}'.format(os.path.basename(dst), src))
                except Exception as e:
                    print('Error linking {} --> {}'.format(os.path.basename(dst), src))
                    print(e)

            assert os.path.islink(dst), '{} is missing link: {}'.format(os.path.basename(dir_path), os.path.basename(dst))


def make_campy(state):
    """ Campy Projects

        Should contain the following sym-links:
        CAMP -> /data/shared/searchdata_wgmlst_adb_cdc_campy_v5_2/CAMP

    """

    shared_dir = '/data/shared'
    labid = state
    camp_dir = '{}_campy'.format(labid)

    dir_path = os.path.join(shared_dir, camp_dir)

    if not os.path.isdir(dir_path):
        # To be safe, we will not create new directories
        # print('{} does not exist'.format(dir_path))
        print('Creating directory: {}'.format(dir_path))
        os.mkdir(dir_path)
    else:
        print('{} already exists!'.format(os.path.basename(dir_path)))

        # Link sources
        src_alleles = os.path.join(shared_dir, 'searchdata_wgmlst_adb_cdc_campy_v5_2/CAMP')
        assert os.path.isdir(src_alleles), 'Unable to find: {}'.format(src_alleles)
        # Link destinations
        alleles_dst = os.path.join(dir_path, 'CAMP')

        links_to_check = { alleles_dst: src_alleles }

        for dst, src in links_to_check.iteritems():
            if os.path.islink(dst):
                print('{} --> {} already exists!'.format(src, dst))
            else:
                try:
                    os.symlink(src, dst)
                    print('Success linking {} --> {}'.format(os.path.basename(dst), src))
                except Exception as e:
                    print('Error linking {} --> {}'.format(os.path.basename(dst), src))
                    print(e)

            assert os.path.islink(dst), '{} is missing link: {}'.format(os.path.basename(dir_path), os.path.basename(dst))


if __name__ == '__main__':

    states = ['CO', 'CT', 'DE', 'FL', 'KS', 'KY', 'MA', 'MD', 'MI', 'MN', 'NY', 'NYC', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'UT', 'VA', 'WA', 'WY']
    # states = ['NYC']

    for state in states:
        print('Working on state: {} meow'.format(state))

        print('{} = {}'.format(state, 'REFID'))
        make_refid(state)
        print('{} = {}'.format(state, 'SALM'))
        make_salm(state)
        print('{} = {}'.format(state, 'LMO'))
        make_lmo(state)
        print('{} = {}'.format(state, 'EC'))
        make_ecoli(state)
        print('{} = {}'.format(state, 'CAMP'))
        make_campy(state)
