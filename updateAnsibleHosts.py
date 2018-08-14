__author__ = 'andrew wilson'

"""MIT License

Copyright (c) 2018 The University of Manchester

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

from collections import defaultdict

from getSheet import getsheet
import conf

env_dev = 'staging'
ca_up = 'Installed, operational'
ca_down = 'Installed, down'
ca_installing = 'Installing'
usb_audio = 'usb'
split_audio = 'split'
bm_embedded_audio = 'embedded'
rtp_muxed_audio = 'muxed'
cc_datapath = 'datapath'
cc_dual_datapath = 'dual datapath'
cc_blackmagic = 'blackmagic'
cc_datapath_axis = 'datapath axis'
cc_none_axis = 'axis'
cc_2_axis = 'axis x2'
no_value = ['None', None]
true_value = ['TRUE', 'True', 'true', 'yes', 'YES', 'Yes', True]
false_value = ['FALSE', 'False', 'false', 'no', 'NO', 'No', False]


def main():
    # sheets = GetSheet()
    sheet_filt = getsheet()
    # figure out the galicaster profile and group by that profile
    groups_list = []
    for ans in sheet_filt:
        # if capture agent is up
        if ans[49] == ca_up or ans[49] == ca_installing:
            group_prefix = '[capture-agents-' + ans[21].replace(' ', '-').strip() + '-' + ans[20].lower().strip()
            # lecturesight and wifi
            if (ans[23] in true_value) and (ans[38] not in no_value):
                hems = group_prefix + '-' + 'lecturesight-wifi]'
                ems = list(ans)
                ems.append(str(hems))
                groups_list.append(ems)
            # lecturesight
            elif ans[23] in true_value:
                hems = group_prefix + '-' + 'lecturesight]'
                ems = list(ans)
                ems.append(str(hems))
                groups_list.append(ems)
            # wifi
            elif ans[38] not in no_value:
                hems = group_prefix + '-' + 'wifi]'
                ems = list(ans)
                ems.append(str(hems))
                groups_list.append(ems)
            # all others
            else:
                hems = group_prefix + ']'
                ems = list(ans)
                ems.append(str(hems))
                groups_list.append(ems)
    master_group_lists = defaultdict(list)

    for v in groups_list:
        master_group_lists[v[-1]].append(v[:])

    # output to text file
    ansible_file_live = open(conf.get_ansible_live(), 'w')
    ansible_file_staging = open(conf.get_ansible_staging(), 'w')

    # adding hosts to file
    for host_group, i in master_group_lists.iteritems():
        ansible_file_live.write(host_group + '\n')
        ansible_file_staging.write(host_group + '\n')
        for L in range(len(i)):

            # staging hosts
            # make sure value is correct string format
            if i[L][28] in no_value or i[L][28] in false_value:
                vl_public = 'false'
            else:
                vl_public = 'true'
            if i[L][29] in no_value or i[L][29] in false_value:
                vl_priv_ep_acl = 'False'
            else:
                vl_priv_ep_acl = i[L][29]
            if i[L][17] in no_value or i[L][17] in false_value:
                blinkstick = 'False'
            else:
                blinkstick = 'True'
            if i[L][24] in no_value or i[L][24] in false_value:
                inverted = 'false'
            else:
                inverted = 'true'
            if i[L][30] in no_value or i[L][30] in false_value:
                tiltlock = 'false'
            else:
                tiltlock = 'true'
            if i[L][38] in no_value or i[L][38] in false_value:
                ssh_port = '22'
            else:
                ssh_port = i[L][38]
            if i[L][4] == env_dev:
                ansible_file_staging.write(
                    '{} ansible_ssh_host={} ansible_ssh_port={} ansible_release_host={} ansible_uom_hostname={} support_group={} home_tunnel_port={} nagios_tunnel_port={} deploy_environment={} name_mask={} ansible_failovermic={} CA_interactive={} oc_default_series={} oc_default_email={} vl_public={} blinkstick={} vapix_inverted={} ptz_tilt_lock={} vl_private_ep_acl={} cam1_host={} cam2_host={} CA_interactive_role={}\n'.format(
                        i[L][3], i[L][40], ssh_port, i[L][40], i[L][43], i[L][7], ssh_port, i[L][39], i[L][4], i[L][5], i[L][16], i[L][25], i[L][27], i[L][30], vl_public, blinkstick, inverted, tiltlock, vl_priv_ep_acl, i[L][45], i[L][46], i[L][26]))
            else:
                # production hosts
                ansible_file_live.write('{} ansible_ssh_host={} ansible_ssh_port={} ansible_release_host={} ansible_uom_hostname={} support_group={} home_tunnel_port={} nagios_tunnel_port={} deploy_environment={} ansible_failovermic={} CA_interactive={} oc_default_series={} oc_default_email={} vl_public={} blinkstick={} vapix_inverted={} ptz_tilt_lock={} vl_private_ep_acl={} cam1_host={} cam2_host={} CA_interactive_role={}\n'.format(
                    i[L][3], i[L][40], ssh_port, i[L][40], i[L][43], i[L][7], ssh_port, i[L][39], i[L][4], i[L][16], i[L][25], i[L][27], i[L][30], vl_public, blinkstick, inverted, tiltlock, vl_priv_ep_acl, i[L][45], i[L][46], i[L][26]))

        ansible_file_live.write('\n')
        ansible_file_staging.write('\n')
    # output the host groups and children to file
    template_end = """


[capture-agents-blackmagic-split-wifi]

[capture-agents-blackmagic-usb-wifi]

[capture-agents-datapath-split-wifi]

[capture-agents-datapath-split-lecturesight]

[capture-agents-datapath-usb-wifi]

[capture-agents-datapath-usb-lecturesight]

[capture-agents-dual-datapath-split-lecturesight]

[capture-agents-dual-datapath-usb-lecturesight]

[capture-agents-datapath-axis-muxed-lecturesight]

[capture-agents-datapath-axis-split-lecturesight]

[capture-agents-datapath-axis-usb-lecturesight]

[capture-agents-blackmagic-split]

[capture-agents-blackmagic-usb]

[capture-agents-blackmagic-embedded]

[capture-agents-datapath-split]

[capture-agents-datapath-usb]

[capture-agents-dual-datapath-split]

[capture-agents-dual-datapath-usb]

[capture-agents-datapath-axis-muxed]

[capture-agents-datapath-axis-split]

[capture-agents-datapath-axis-usb]

[capture-agents-axis-x2-muxed]

[capture-agents-axis-muxed]

[capture-agents-v4l2-x2-axis-muxed]

[capture-agents-v4l2-split]

[capture-agents-v4l2-usb]



[capture-agents-blackmagic-split:children]
capture-agents-blackmagic-split-wifi

[capture-agents-blackmagic-usb:children]
capture-agents-blackmagic-usb-wifi

[capture-agents-datapath-split:children]
capture-agents-datapath-split-wifi
capture-agents-datapath-split-lecturesight

[capture-agents-datapath-usb:children]
capture-agents-datapath-usb-wifi
capture-agents-datapath-usb-lecturesight

[capture-agents-dual-datapath-split:children]
capture-agents-dual-datapath-split-lecturesight

[capture-agents-dual-datapath-usb:children]
capture-agents-dual-datapath-usb-lecturesight

[capture-agents-datapath-axis-muxed:children]
capture-agents-datapath-axis-muxed-lecturesight

[capture-agents-datapath-axis-split:children]
capture-agents-datapath-axis-split-lecturesight

[capture-agents-datapath-axis-usb:children]
capture-agents-datapath-axis-usb-lecturesight

[capture-agents-blackmagic:children]
capture-agents-blackmagic-split
capture-agents-blackmagic-usb
capture-agents-blackmagic-embedded

[capture-agents-datapath:children]
capture-agents-datapath-split
capture-agents-datapath-usb
capture-agents-dual-datapath-split
capture-agents-dual-datapath-usb
capture-agents-datapath-axis-muxed
capture-agents-datapath-axis-split
capture-agents-datapath-axis-usb

[capture-agents-axis:children]
capture-agents-axis-x2-muxed
capture-agents-axis-muxed

[capture-agents-v4l2:children]
capture-agents-v4l2-x2-axis-muxed
capture-agents-v4l2-split
capture-agents-v4l2-usb

[capture-agents:children]
capture-agents-blackmagic
capture-agents-datapath
capture-agents-axis
capture-agents-v4l2"""

    ansible_file_live.write(template_end)
    ansible_file_staging.write(template_end)
    ansible_file_live.close()
    ansible_file_staging.close()
    print str(len(groups_list)) + ' Capture Agent hosts updated'

if __name__ == '__main__':
    main()