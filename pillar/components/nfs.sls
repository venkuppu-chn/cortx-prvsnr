nfs:
  local_addr: "{{ grains['ip_interfaces']['data0'][0] }}@tcp:12345:44:301"
  ha_addr: "{{ grains['ip_interfaces']['data0'][0] }}@tcp:12345:45:1"
  profile: "0x7000000000000001:1"
  proc_fid: "0x7200000000000000:0"
  index_dir: /tmp
  kvs_fid: "0x780000000000000b:1"
