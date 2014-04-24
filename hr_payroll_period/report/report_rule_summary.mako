<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    <br />
    <br />
    <br />
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