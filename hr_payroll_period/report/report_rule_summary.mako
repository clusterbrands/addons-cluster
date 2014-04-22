<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <div align="right">${"Date: "+formatLang(time.strftime('%Y-%m-%d'),date=True)}</div>  
    <table>
        <tr>
            <td style="vertical-align:middle;">
                ${ helper.embed_image('png',company.logo,120,55)|n }
            </td>
            <td>
                <div>
                    <span style="font-size:16px">
                        <b>${ company.name }</b>
                    </span><br/>
                    <span style="font-size:8px">
                       RIF: J-40135625-7
                    </span>
                </div>
            </td>
        </tr>       
    </table>        
    <center><h3><u>${_("Salary Rules Summary")}</u></h3></center>
    <br/>
    <table class="concept_table" width="100%">
        <thead>
            <tr>
                <th style="text-align:left;" width ="10%">${_("Code")}</th>
                <th style="text-align:left;" width ="70%">${_("Salary Rule Category")}</th>
                <th style="text-align:right;" width ="20%" >${_("Total")}</th>
            </tr>
        </thead>
        %for line in (get_details_by_rule_category(objects)):
            <tbody>
                <tr>
                    <td style="text-align:left;">
                        %if line['level'] !=0:
                            ${line.get('code') or '' |entity}
                        %else:
                            <b>${line.get('code') or '' |entity}</b>
                        %endif
                    </td>
                    <td style="text-align:left;">
                        %if line['level'] !=0:
                            ${line.get('name') or '' |entity} 
                        %else:
                            <b>${line.get('name') or '' |entity}</b>
                        %endif
                    </td>
                    <td style="text-align:right;">
                        %if line['level'] !=0:                       
                            ${line.get('total') or 0.0 |entity}
                        %else: 
                            <b>${line.get('total') or 0.0 |entity}</b>
                        %endif                       
                    </td>
                </tr>
            </tbody>
        %endfor
    </table>   
</body>
</html>