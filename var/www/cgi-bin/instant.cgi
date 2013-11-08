#!/usr/bin/perl

use strict;

use CGI;
use CGI::Carp qw(fatalsToBrowser);
use Data::Dumper;
use PDF::API2;

my $q = new CGI;

my %month_points = (
    January => {
        start => 233,
        end   => 380
    },
    February => {
        start => 229,
        end   => 383
    },
    March => {
        start => 236,
        end   => 376
    },
    April => {
        start => 240,
        end   => 372
    },
    May => {
        start => 242,
        end   => 370
    },
    June => {
        start => 241,
        end   => 371
    },
    July => {
        start => 242,
        end   => 370
    },
    August => {
        start => 235,
        end   => 377
    },
    September => {
        start => 226,
        end   => 386
    },
    October => {
        start => 233,
        end   => 379
    },
    Novemeber => {
        start => 225,
        end   => 387
    },
    December => {
        start => 227,
        end   => 384
    }
);

if ($q->param('action')) {
    my $params    = $q->Vars;
    my $file_name = "Salary Slip $params->{month} $params->{year}.pdf";

    create_payslip($params, $file_name);
    if (-e "./pdf/$file_name") {
        print $q->header(-type => 'application/x-pdf', -attachment => $file_name);

        open (DOWNLOAD, "<./pdf/$file_name") or die $!;
        while (<DOWNLOAD>) {
            print;
        }
        close DOWNLOAD;

        unlink "./pdf/$file_name";
    }
}

print $q->header;

my ($month, $year) = (localtime)[4 .. 5];
$year += 1900;
$month--; # The previous month is selected by default

my %selected;
$selected{month}{$month} = qq{ selected="selected"};

my @months = qw(January February March April May June July August September
                October Novemeber December);
my $months;
$months .= qq{<option value="$months[$_]"$selected{month}{$_}>$months[$_]</option>\n} for 0 .. 11;

my $years = qq{<option value="$year">$year</option>\n};
for (1 .. 4) {
    $year--;
    $years .= qq{<option value="$year">$year</option>\n};
}

print qq{
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en">
    <head>
        <title>Nuventure Technolog Solutions</title>
        <link rel="stylesheet" type="text/css" href="/payslip/css/dhtmlgoodies_calendar.css" />
        <script type="text/javascript" src="/payslip/js/prototype.js"></script>
        <script type="text/javascript" src="/payslip/js/dhtmlgoodies_calendar.js"></script>
        <script type="text/javascript">
            function validate_form() {
                var elements = ['employee_code', 'employee_name', 'designation'];
                for (var i = 0; i < elements.length; i++) {
                    if (validate_element(elements[i]) == false) return;
                }

                document.payslip.submit();
            }

            function validate_element(id) {
                var obj = document.getElementById(id);
                var val = obj.value;
                var tit = obj.title;
                if (val == null || val == '' || val.match(/^\\s+\$/)) {
                    alert('Please enter ' + tit);
                    obj.focus();
                    return false;
                }

                return true;
            }

            function validate_amount(e) {
                var charCode = e.which || event.keyCode;
                if (charCode > 31 && charCode != 46 && (charCode < 48 || charCode > 57))
                    return false;
            
                return true;
            }
        </script>
    </head>
    <body>
        <form name="payslip" action="" method="post">
            <table>
                <tr>
                    <td>Employee Code</td>
                    <td><input type="text" name="employee_code" id="employee_code" title="Employee Code" /></td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td><input type="text" name="employee_name" id="employee_name" title="Employee Name" /></td>
                </tr>
                <tr>
                    <td>Designation</td>
                    <td><input type="text" name="designation" id="designation" title="Designation" /></td>
                </tr>
                <tr>
                    <td>Date of Joining</td>
                    <td>
                        <input type="text" name="joining_date" id="joining_date" title="Date of Joining" readonly="readonly" />
                        <img src="/payslip/images/calander.gif" style="cursor:pointer;" onclick="displayCalendar(\$('joining_date'), 'dd-mm-yyyy', this); return false;" />
                    </td>
                </tr>
                <tr>
                    <td>Payslip Month & Year</td>
                    <td>
                        <select name="month" id="month" title="Month">
                            $months
                        </select>
                        <select name="year" id="year" title="Year">
                            $years
                        </select>
                    </td>
                </tr>
                <tr><td colspan="2"><b>Earnings</b></td></tr>
                <tr>
                    <td>Basic</td>
                    <td><input type="text" name="basic" id="basic" title="Basic" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>HRA</td>
                    <td><input type="text" name="hra" id="hra" title="HRA" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Conveyance Allowance</td>
                    <td><input type="text" name="conveyance_allowance" id="conveyance_allowance" title="Conveyance Allowance" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Medical Allowance</td>
                    <td><input type="text" name="medical_allowance" id="medical_allowance" title="Medical Allowance" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Special Allowance</td>
                    <td><input type="text" name="special_allowance" id="special_allowance" title="Special Allowance" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Mobile Allowance</td>
                    <td><input type="text" name="mobile_allowance" id="mobile_allowance" title="Mobile Allowance" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Other Allowance</td>
                    <td><input type="text" name="other_allowance" id="other_allowance" title="Other Allowance" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr><td colspan="2"><b>Deductions</b></td></tr>
                <tr>
                    <td>Provident Fund</td>
                    <td><input type="text" name="pf" id="pf" title="PF" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Professional Tax</td>
                    <td><input type="text" name="professional_tax" id="professional_tax" title="Professional Tax" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Tax Deducted at Source</td>
                    <td><input type="text" name="tds" id="tds" title="TDS" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td>Employee Welfare Fund</td>
                    <td><input type="text" name="welfare_fund" id="welfare_fund" title="Employee Welfare Fund" size="8" onkeypress="return validate_amount(event);" /></td>
                </tr>
                <tr>
                    <td colspan="2" align="center">
                        <input type="button" value="Submit" onclick="validate_form();" />
                        <input type="hidden" name="action" value="submit" />
                    </td>
                </tr>
            </table>
        </form>
    </body> 
</html>
};

sub create_payslip {
    my ($params, $file_name) = @_;

    # Earnings
    my $basic                = sprintf("%.2f", $params->{basic});
    my $hra                  = sprintf("%.2f", $params->{hra});
    my $conveyance_allowance = sprintf("%.2f", $params->{conveyance_allowance});
    my $medical_allowance    = sprintf("%.2f", $params->{medical_allowance});
    my $special_allowance    = sprintf("%.2f", $params->{special_allowance});
    my $mobile_allowance     = sprintf("%.2f", $params->{mobile_allowance});
    my $other_allowance      = sprintf("%.2f", $params->{other_allowance});

    # Deductions
    my $pf               = sprintf("%.2f", $params->{pf});
    my $professional_tax = sprintf("%.2f", $params->{professional_tax});
    my $tds              = sprintf("%.2f", $params->{tds});
    my $welfare_fund     = sprintf("%.2f", $params->{welfare_fund});

    # Total
    my $total_earnings   = sprintf("%.2f", $basic + $hra + $conveyance_allowance + $medical_allowance + $special_allowance + $mobile_allowance + $other_allowance);
    my $total_deductions = sprintf("%.2f", $pf + $professional_tax + $tds + $welfare_fund);
    my $net_amount       = sprintf("%.2f", $total_earnings - $total_deductions);

    my ($column_1_x, $column_2_x, $column_3_x) = (75, 310, 530);
    my $row_height  = 20;
    my $y;

    my $pdf = PDF::API2->new;

    my %font = (
        Courier => {
            Normal => $pdf->corefont('Courier',         -encoding => 'latin1'),
            Bold   => $pdf->corefont('Courier-Bold',    -encoding => 'latin1'),
            Italic => $pdf->corefont('Courier-Oblique', -encoding => 'latin1'),
        },
        Times => {
            Normal => $pdf->corefont('Times',        -encoding => 'latin1'),
            Bold   => $pdf->corefont('Times-Bold',   -encoding => 'latin1'),
            Italic => $pdf->corefont('Times-Italic', -encoding => 'latin1'),
        },
    );

    my $page = $pdf->page;
    $page->mediabox(612, 792);

    my $gfx = $page->gfx;

    my $logo = $pdf->image_png("logo.png");
    $gfx->image($logo, 70, 650, 1);

    my $text = $page->text;
    $text->fillcolor('black');

    my $line = $page->gfx;

    $text->font($font{Times}{Bold}, 12);

    $text->translate(306, 610);
    $text->text_center("Salary Slip for $params->{month} $params->{year}");
    $line->move($month_points{$params->{month}}{start}, 606);
    $line->line($month_points{$params->{month}}{end}, 606);

    # Rectangle
    my $box = $page->gfx;
    $box->rectxy(70, 150, 550, 600);
    $box->stroke;

    # First horizontal line
    $line->move(70, 490);
    $line->line(550, 490);

    # First vertical line
    $line->move(305, 600);
    $line->line(305, 490);

    # Second horizontal line
    $line->move(70, 470);
    $line->line(550, 470);

    # Second vertical line
    $line->move(420, 490);
    $line->line(420, 150);

    $line->stroke;

    $text->font($font{Courier}{Normal}, 12);
    $y = 580;

    $text->translate($column_1_x, $y);
    $text->text('Employee Code');

    $text->translate($column_2_x, $y);
    $text->text($params->{employee_code});

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Name');

    $text->translate($column_2_x, $y);
    $text->text($params->{employee_name});

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Designation');

    $text->translate($column_2_x, $y);
    $text->text($params->{designation});

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Location');

    $text->translate($column_2_x, $y);
    $text->text('Kochi');

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Date of Joining');

    $text->translate($column_2_x, $y);
    $text->text($params->{joining_date});

    $text->font($font{Courier}{Bold}, 12);

    $text->translate(250, 477);
    $text->text_center('Particulars');

    $text->translate(490, 477);
    $text->text_center('Rs.');

    $text->translate(250, 457);
    $text->text_center('A. Earnings');

    $text->translate(250, 277);
    $text->text_center('B. Deductions');


    $text->translate(250, 157);
    $text->text_center('Net Salary A - B');

    $text->translate($column_3_x, 157);
    $text->text_right($net_amount);

    $text->font($font{Courier}{Normal}, 12);
    $y = 437;

    $text->translate($column_1_x, $y);
    $text->text('Basic');

    $text->translate($column_3_x, $y);
    $text->text_right($basic);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('HRA');

    $text->translate($column_3_x, $y);
    $text->text_right($hra);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Conveyance Allowance');

    $text->translate($column_3_x, $y);
    $text->text_right($conveyance_allowance);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Medical Allowance');

    $text->translate($column_3_x, $y);
    $text->text_right($medical_allowance);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Special Allowance');

    $text->translate($column_3_x, $y);
    $text->text_right($special_allowance);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Mobile Allowance');

    $text->translate($column_3_x, $y);
    $text->text_right($mobile_allowance);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Other Allowance');

    $text->translate($column_3_x, $y);
    $text->text_right($other_allowance);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Total Earnings');

    $text->translate($column_3_x, $y);
    $text->text_right($total_earnings);

    $y -= 40;

    $text->translate($column_1_x, $y);
    $text->text('Provident Fund');

    $text->translate($column_3_x, $y);
    $text->text_right($pf);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Professional Tax');

    $text->translate($column_3_x, $y);
    $text->text_right($professional_tax);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Tax Deducted at Source');

    $text->translate($column_3_x, $y);
    $text->text_right($tds);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Employee Welfare Fund');

    $text->translate($column_3_x, $y);
    $text->text_right($welfare_fund);

    $y -= $row_height;

    $text->translate($column_1_x, $y);
    $text->text('Total Deductions');

    $text->translate($column_3_x, $y);
    $text->text_right($total_deductions);

    $text->font($font{Times}{Normal}, 10);
    $text->translate(490, 100);
    $text->text_center('Anju Anto');
    $text->translate(490, 88);
    $text->text_center('HR Manager');


    # Page number
    #$text->fillcolor('#696969');
    #$text->translate(306, 50);
    #$text->text_center('Page 1');

    # Footer start
    my $footer_box = $page->gfx;
    $footer_box->rectxy(0, 30, 612, 0);
    $footer_box->fillcolor('#1A3459');
    $footer_box->fill;

    my $footer_text = $page->text;
    $footer_text->font($font{Times}{Normal}, 8);
    $footer_text->fillcolor('white');
    $footer_text->translate(306, 10);
    $footer_text->text_center('1st Floor, Apex Buildings, Ashoka Road, Kaloor, Kochi-682017, India. Tel: +91-484-6462287, Fax: +91-484-4015524, Email: info@nuventure.in, Website: www.nuventure.in');
    # Footer end

    $pdf->saveas("./pdf/$file_name");
    $pdf->end;
}
