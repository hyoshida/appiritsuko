# -*- encoding: utf-8 -*-

Encoding::default_external = Encoding::UTF_8

# init gems
require 'bundler'
Bundler.require

require 'csv'

DATA_DIR = '/home/yoshida/.appiritsko'

def load_member_map
  member_map = {}
  CSV.foreach('members.tsv', col_sep: "\t") do |(key,value)|
    member_map[key] = value
  end
  member_map
end

def init_talk_map
  member_map = load_member_map
  member_map.values.inject({}) do |result,member_name|
    result[member_name] = 0
    result
  end
end

def load_talk_map(filepath)
  member_map = load_member_map
  ini = IniFile.load(filepath)
  ini[:counter].inject(init_talk_map) do |result,(key,value)|
    member_name = member_map[key]
    result[member_name] = value
    result
  end
end

def talk_filenames
  Dir.glob("#{DATA_DIR}/*.ini.*").map do |filepath|
    filepath
  end.sort
end

def load_talk_maps_with_date
  talk_filenames.inject({}) do |result,filepath|
    date = /^.+(\d{8})$/.match(filepath).to_a.last
    result[date] = load_talk_map(filepath) unless date.nil?
    result
  end
end

def build_table
  talk_maps_with_date = load_talk_maps_with_date
  talk_maps_with_date.inject({}) do |result,(date,talk_map)|
    talk_map.each do |member_name,count|
      result[member_name] ||= {}
      result[member_name].update(date => count)
    end
    result
  end
end

def month_and_day(date_string)
  require 'date'
  date = Date.parse(date_string)
  date.strftime("%m-%d\n#{%w(日 月 火 水 木 金 土)[date.wday]}")
end

get '/' do
  @table = build_table
  slim :index
end

__END__

@@ index
script type="text/javascript" src="js/jquery.js"
script type="text/javascript" src="js/visualize.jQuery.js"
link type="text/css" rel="stylesheet" href="css/visualize.css"
link type="text/css" rel="stylesheet" href="css/visualize-light.css"
javascript:
  $(function(){
    var colors = [ '#BE1E2D', '#666699', '#92D5EA', '#EE8310', '#8D10EE', '#5A3B16', '#26A4ED', '#F45A90', '#E9E744', '#0E8800', '#736BFF', '#4E4E4E', '#A2A2A2', '#AEDF8C' ]
    $('table').visualize({
      title: '過去のおしゃべりさんをグラフにしてみました！',
      type: 'line',
      width: '#{@table.values.first.keys.size*50}px',
      height: '580px',
      colors: colors
    });
  });
css:
  html {
    margin: 0;
    padding: 0;
    padding-left: 420px;
    background: #A6EA6D url('ritsuko.jpg') -100px 0 no-repeat;
  }
  body {
    padding-right: 50px;
  }
table style="display: none"
  tr
    th &nbsp;
    - count_map_with_date = @table.values.first
    - count_map_with_date.keys.each do |date|
      th.row = month_and_day(date)
  - @table.each do |member_name,count_map_with_date|
    tr
      th.col = member_name
      - count_map_with_date.values.each do |count|
        td = count
