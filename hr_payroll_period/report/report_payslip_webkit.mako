<html>
<head>
    <style type="text/css">
        ${css}
    </style>
</head>
<body>
    %for o in objects :
        <br/>
        <br/>
        <center><h2><u>${("Pay Slip")}</u></h2></center>
        %if o.credit_note!=False:
            <center><h2>${("Credit")}</h2></center>
            <center><h2>${("Note")}</h2></center>
        %endif
        <!-- <center>(${o.name or '' | entity})</center> -->
        <table class="basic_table" width="100%" align="center">
            <tr>
                <td width="20%">
                    <b>${_("Name")} </b>
                </td>
                <td width="30%">
                    ${o.employee_id.name or '' |entity}
                </td>
                <td width="20%">
                    <b>${_("Designation")} </b>
                </td>
                <td width="30%">
                    ${o.employee_id.job_id.name or ''|entity}
                </td>
            </tr>
            <tr>
                <td style="text-align:left;">
                    <b>${_("Address")} </b></br></br></br>
                </td>
                <td colspan="3" style="text-align:left">
                    ${o.employee_id.address_home_id and o.employee_id.address_home_id.name or ''|entity}<br/>
                    %if o.employee_id.address_home_id.street:
                        ${o.employee_id.address_home_id.street or ''|entity},<br/>
                    %endif
                    %if o.employee_id.address_home_id.street2:
                        ${o.employee_id.address_home_id.street2 or ''|entity},<br/>
                    %endif
                    %if o.employee_id.address_home_id:
                        ${o.employee_id.address_home_id.zip or ''|entity} ${o.employee_id.address_home_id.city or ''|entity},<br/>
                    %endif
                    %if o.employee_id.address_home_id.country_id:
                        ${o.employee_id.address_home_id.country_id.name or ''|entity},<br/>
                    %endif
                    %if o.employee_id.address_home_id.phone:
                        ${o.employee_id.address_home_id.phone or ''|entity},<br/>
                    %endif
                </td>
            </tr>
            <tr>
                <td>
                    <b>${_("Email")} </b>
                </td>
                <td>
                    ${o.employee_id.work_email or '' |entity}
                </td>
                <td>
                    <b>${_("Identification No")} </b>
                </td>
                <td>
                    ${o.employee_id.identification_id or ''|entity}
                </td>           
            </tr>
            <tr>
                <td>
                    <b>${_("Reference")} </b>
                </td>
                <td>
                    ${o.number or ''|entity}
                </td>
                <td>
                    <b>${_("Bank Account")} </b>
                </td>
                <td>
                    ${o.employee_id.otherid or ''|entity}
                </td>           
            </tr>
            <tr>
                <td>
                    <b>${_("Date From")} </b>
                </td>
                <td>
                    ${formatLang(o.date_from,date=True) or ''|entity}
                </td>
                <td>
                    <b>${_("Date To")} </b>
                </td>
                <td>
                    ${formatLang(o.date_to,date=True) or ''|entity}
                </td>           
            </tr>
        </table>
        <br/><br/>
        <table class="list_table"  width="100%">
            <thead>
                <tr>
                    <th style="text-align:left;">${_("Code")}</th>
                    <th style="text-align:left;">${_("Name")}</th>
                    <th style="text-align:right;">${_("Quantity/Rate")}</th>
                    <th style="text-align:right;" >${_("Amount")}</th>
                    <th style="text-align:right;" >${_("Total")}</th>
                </tr>
            </thead>
            %for line in (get_payslip_lines(o.line_ids)):
                <tbody>
                <tr>
                    <td style="text-align:left;">
                        ${line.code or ''|entity}
                     </td>
                    <td style="text-align:left;">
                        ${line.name or '' |entity} 
                    </td>
                    <td>
                        ${formatLang(line.quantity) or '' |entity} 
                    </td>
                    <td style="text-align:right;">
                        ${formatLang(line.amount) or '' |entity} 
                    </td>
                    <td style="text-align:right;">
                        ${formatLang(line.total, currency_obj = o.company_id and o.company_id.currency_id) or 0.0 |entity}
                    </td>
                </tr>
                </tbody>
            %endfor
        </table>
        <br/>
        <br/>
        <table class="sign"  width="100%">
            <tr>
                <td  style="text-align:right;"><b>${_("Authorized Signature")}</b></td>
            </tr>
        </table>
        <p style="page-break-after:always"></p>
    %endfor 
</body>
</html>