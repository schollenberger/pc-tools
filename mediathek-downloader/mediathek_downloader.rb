#!/usr/bin/ruby
require 'optparse'
require 'logger'

# This program reads a text file and extracts the neccessary information to
# download videos from web site MediathekViewWeb .

class InternalError < StandardError
  #  puts "EXCEPTION: Internal Error, does not need to have Stack tracing, exit_code is set.
end


class MediathekDownloader
  def initialize(filename)
    @textfile = filename
  end

  def analyse
    raise InternalError, "Global logger variable not defined." if not $logger
    logger = $logger
    logger.debug "Starting..."
    file = File.open(@textfile)
    datamap = file.readlines.map(&:chomp)
    file.close

    logger.info "Media file line count = #{datamap.size}"
    # logger.debug datamap.class
    # logger.debug datamap.flatten

    download_list = Array.new
    readme_list = Array.new
    lineno = 0

    count = 0
    sender = ""
    title = ""
    title_filename = ""
    seq = ""
    comment = ""
    episode = ""
    m_date = ""
    m_time = ""
    m_duration = ""

    datamap.each do |entry|
      lineno += 1
      if entry.strip.start_with?("#")
        logger.debug "Ignoring comment <#{entry}>"
        next
      elsif entry.strip.empty?
        logger.debug "Ignoring empty line"
        next
      elsif entry.strip.start_with?("---")
        logger.info "--- New entry on line #{lineno} - closing up old one..."
        if !sender.empty? && !title.empty? && !episode.empty? && !seq.empty? &&
           !comment.empty?
          logger.info "Completed entry - #{sender} - #{title} - #{episode} - #{seq} - #{m_date} - #{m_time} - #{m_duration}"
          logger.info "Completed comment: <#{comment}>"
          logger.info "---"
          if seq == "_"
            readme_filename = "#{title_filename}-readme.txt"
          else
            readme_filename = "#{title_filename}-#{seq}-readme.txt"
          end
          readme_list << [readme_filename.clone, sender.clone, title.clone,
                          episode.clone, seq.clone, m_date.clone, m_time.clone,
                          m_duration.clone, comment.clone]
          # logger.info "Writing download info file to: #{readme_filename}"
        else
          logger.warn "** Incomplete previous entry:  - #{sender} - #{title} - #{episode} - #{seq}"
          logger.warn "** Comment on incomplete entry: <#{comment}>"
          # looking for element in download_list
          _delete_list = Array.new
          download_list.each do |entry|
            if entry[0].match?(title_filename)
              logger.debug "** Marking element <#{entry[0]}> for deletion from download list."
              _delete_list << entry
            end
          end
          _delete_list.each do |entry|
            logger.info "** Deleting entry <#{entry[0]}> from download_list."
            download_list.delete(entry)
          end
        end
        count = 0
        sender.clear
        title.clear
        title_filename.clear if title_filename
        seq.clear
        comment.clear
        episode.clear
        m_date.clear
        m_time.clear
        m_duration.clear
      else
        count += 1
      end

      #logger.debug "Analysing line #{lineno} - count #{count}..."
      case count
      when 0
         # do nothing - separator
      when 1  # Sender
        sender = entry
        # puts "Sender: #{sender}"
      when 2 # Title
        title = entry
        title_filename = title.gsub(' ', '_')
        logger.info "Title:   #{title} - Title filename: #{title_filename}"
      when 3  # Episode
        episode = entry
        logger.info "Episode: #{episode}"
      when 4
        logger.debug "Seq field: #{entry} of class #{entry.class}"
        str = entry.clone
        ["(", ")", "/"].each do |s_str|
          if ! str
            logger.error "Error in parsing sequence string <#{entry}> on replace string <#{s_str}>"
            str = ""
            break
          end
          str.sub!(s_str, "")
        end
        if str and !str.empty?
          seq = str
          logger.warn "Invalid format of sequence number <#{str}> on line #{lineno}" if !seq.match?('S\d\dE\d\d')
        else
          logger.warn "Parsing sequence entry <#{entry}> returned nothing. Using underscore char."
          seq = "_"
        end
        logger.info "Sequence nummer: <#{seq}>"
      when 5
        m_date,m_time,m_duration = entry.split(" ")
        logger.debug "Date: #{m_date} - Time: #{m_time} - Duration #{m_duration}"
      when 6
        comment = entry
        logger.info "Comment line found with #{comment.length()} characters."
        # logger.info "Comment: <#{comment}>"
      else
        if entry and entry.strip.length() > 0
          if entry.start_with?("http")
            url = entry.strip
            logger.debug "URL: #{url}"
          else
            logger.error "Expected http URL #{count} line #{lineno} - found <#{entry}>"
            next
          end
          if url.end_with?(".mp4")
            logger.debug "** movie download ..."
            url_filename = url[url.rindex('/')+1 .. -1]
            logger.info "Found *movie* URL wih filename: #{url_filename}"
            movie_quality = "-not_defined"
            if url_filename.match?("_960x") or url_filename.match?("\\.l\\.") or url_filename.match?("_2360k_")
              logger.info "Movie quality = medium"
              movie_quality = "-medium"
            elsif url_filename.match?("_1920x") or url_filename.match?("\\.xxl\\.") or url_filename.match?("_3360k_") or url_filename.match?("_3328k_")
              logger.info "Movie quality = high"
              movie_quality = "-high"
            else
              logger.warn "Could not detect movie quality"

              movie_quality = ""
            end
            if seq == "_"
              movie_name = "#{title_filename}#{movie_quality}.mp4"
            else
              movie_name = "#{title_filename}-#{seq}#{movie_quality}.mp4"
            end
            logger.info "Storing movie URL under filename: <#{movie_name}>"
            download_list << [movie_name.clone, url.clone]

          elsif url.match?("subtitle")
            logger.debug "** subtitle download ..."
            subtitle_filename = url[url.rindex('/')+1 .. -1]
            logger.info "Found *subtitle* URL wih filename: #{subtitle_filename}"
            if seq == "_"
              subtitle_name = "#{title_filename}-subtitle.xml"
            else
              subtitle_name = "#{title_filename}-#{seq}-subtitle.xml"
            end
            logger.info "Storing subtitle URL under filename <#{subtitle_name}>"
            download_list << [subtitle_name.clone, url.clone]
          else
            logger.warn "Could not identify URL type for < #{url}> (no mp4/subtitle)."
          end
        end
      end
    end

    return download_list, readme_list
  end

  def download(download_list, overwrite = false)
    logger = $logger
    logger.debug "Starting download ..."

    download_list.each do |entry|
      fn, url = entry
      if File.exists?(fn) and ! overwrite
         logger.warn "Skipping download of file <#{fn}> that already exists, use overwrite option if needed"
      else
         command = "wget -O #{fn} #{url}"
         logger.debug "Downloading  URL: #{url}"
         logger.info "Downloading to file <#{fn}>"
         rstatus = system(command)
         #rstatus = true
         logger.error "Failed with system command <#{command}>!"  if ! rstatus
       end
    end
  end

  def write_readme(readme_list)
    logger = $logger
    logger.debug "Start writing readme files ..."

    readme_list.each do |entry|
      r_filename,r_sender,r_titel,r_thema,r_folge,
      r_datum,r_zeit,r_dauer,r_comment = entry
      logger.info "Writing readme to file: #{r_filename}..."
      File.open(r_filename, "w") do |f|
        f.puts "Readme:    #{r_filename}"
        f.puts "           Download from MediathekViewWeb https://mediathekviewweb.de/"
        f.puts
        f.puts "Sender:    #{r_sender}"
        f.puts "Titel:     #{r_titel} "
        f.puts "Thema:     #{r_thema}"
        f.puts "Folge:     #{r_folge}   (SxxEyy = Staffel xx Episode yy)" if r_folge && !r_folge.empty?
        f.puts "Sendezeit: #{r_datum} #{r_zeit}"
        f.puts "Dauer:     #{r_dauer} min:sec"
        f.puts "Beschreibung:"
        f.puts "#{r_comment}"
        f.puts
      end
    end
  end
end

if __FILE__ == $0
  $logger = Logger.new(STDERR) unless $logger
  $logger.level = Logger::INFO
#  $logger.level = Logger::DEBUG
  $stdout.sync =  true

  if ARGV.size == 1
    media_file = ARGV[0].to_s
  else
    puts "Requires exactly one argument which is the media file to parse."
    puts "After parsing the options, #{ARGV.size} argumetns remained. They are #{ARGV}."
    puts "Exiting with error code -1."
    exit -1
  end

  if !File.file?(media_file)
    puts "Media file <#{media_file}> doesn't exist. Exiting with error code -2."
    exit -1
  end

  obj = MediathekDownloader.new(media_file)

  download_list, readme_list = obj.analyse

  #puts "Download list:"
  ##puts download_list
  #download_list.each do |entry|
  #  puts entry
  #  puts "++++++++"
  #end
  #puts "-----------------------"
  #puts "Readme list:"
  ##puts readme_list
  #readme_list.each do |entry|
  #  puts entry
  #  puts "+++"
  #end
  #puts "-----------------------"

  obj.download(download_list)
  obj.write_readme(readme_list)
end
